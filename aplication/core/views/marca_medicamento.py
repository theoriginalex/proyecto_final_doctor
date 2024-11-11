from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.models import MarcaMedicamento
from aplication.core.forms.marca_medicamento import MarcaMedicamentoForm  # Asegúrate de tener un formulario para MarcaMedicamento
from doctor.utils import save_audit
from django.db.models import Q

class MarcaMedicamentoListView(ListView):
    template_name = "core/marca_medicamento/list.html"
    model = MarcaMedicamento
    context_object_name = 'marcas_medicamento'
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
        context['title1'] = "Consulta de Marcas de Medicamento"
        return context

class MarcaMedicamentoCreateView(CreateView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamento/form.html'
    form_class = MarcaMedicamentoForm
    success_url = reverse_lazy('core:marca_medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Ingresar Marca de Medicamento'
        context['grabar'] = 'Grabar Marca de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        marca_medicamento = self.object
        save_audit(self.request, marca_medicamento, action='A')
        messages.success(self.request, f"Éxito al crear la marca de medicamento {marca_medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class MarcaMedicamentoUpdateView(UpdateView):
    model = MarcaMedicamento
    template_name = 'core/marca_medicamento/form.html'
    form_class = MarcaMedicamentoForm
    success_url = reverse_lazy('core:marca_medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Modificar Marca de Medicamento'
        context['grabar'] = 'Actualizar Marca de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        marca_medicamento = self.object
        save_audit(self.request, marca_medicamento, action='M')
        messages.success(self.request, f"Éxito al modificar la marca de medicamento {marca_medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class MarcaMedicamentoDeleteView(DeleteView):
    model = MarcaMedicamento
    success_url = reverse_lazy('core:marca_medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['grabar'] = 'Eliminar Marca de Medicamento'
        context['description'] = f"¿Desea eliminar la marca de medicamento: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar la marca de medicamento {self.object.nombre}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class MarcaMedicamentoDetailView(DetailView):
    model = MarcaMedicamento

    def get(self, request, *args, **kwargs):
        marca_medicamento = self.get_object()
        data = {
            'id': marca_medicamento.id,
            'nombre': marca_medicamento.nombre,
            'descripcion': marca_medicamento.descripcion,
            'activo': marca_medicamento.activo,
        }
        return JsonResponse(data)
