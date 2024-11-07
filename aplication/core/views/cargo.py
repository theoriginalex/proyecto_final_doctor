from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.models import Cargo
from aplication.core.forms.cargo import CargoForm
from doctor.utils import save_audit
from django.db.models import Q

class CargoListView(ListView):
    template_name = "core/cargo/list.html"
    model = Cargo
    context_object_name = 'cargos'
    paginate_by = 10

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query.add(Q(nombre__icontains=q) | Q(descripcion__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SaludSync"
        context['title1'] = "Consulta de Cargos"
        return context

class CargoCreateView(CreateView):
    model = Cargo
    template_name = 'core/cargo/form.html'
    form_class = CargoForm
    success_url = reverse_lazy('core:cargo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Ingresar Cargo'
        context['grabar'] = 'Grabar Cargo'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        cargo = self.object
        save_audit(self.request, cargo, action='A')
        messages.success(self.request, f"Éxito al crear el cargo {cargo.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class CargoUpdateView(UpdateView):
    model = Cargo
    template_name = 'core/cargo/form.html'
    form_class = CargoForm
    success_url = reverse_lazy('core:cargo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Modificar Cargo'
        context['grabar'] = 'Actualizar Cargo'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        cargo = self.object
        save_audit(self.request, cargo, action='M')
        messages.success(self.request, f"Éxito al modificar el cargo {cargo.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class CargoDeleteView(DeleteView):
    model = Cargo
    success_url = reverse_lazy('core:cargo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['grabar'] = 'Eliminar Cargo'
        context['description'] = f"¿Desea eliminar el cargo: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el cargo {self.object.nombre}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class CargoDetailView(DetailView):
    model = Cargo

    def get(self, request, *args, **kwargs):
        cargo = self.get_object()
        data = {
            'id': cargo.id,
            'nombre': cargo.nombre,
            'descripcion': cargo.descripcion,
            'activo': cargo.activo,
        }
        return JsonResponse(data)
