from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.models import CategoriaExamen
from aplication.core.forms.categoria_examen import CategoriaExamenForm
from doctor.utils import save_audit
from django.db.models import Q

class CategoriaExamenListView(ListView):
    template_name = "core/categoria_examen/list.html"
    model = CategoriaExamen
    context_object_name = 'categorias_examen'
    paginate_by = 10

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query.add(Q(nombre__icontains=q) | Q(descripcion__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Gestión de Categorías de Exámenes"
        context['title1'] = "Consulta de Categorías de Exámenes"
        return context

class CategoriaExamenCreateView(CreateView):
    model = CategoriaExamen
    template_name = 'core/categoria_examen/form.html'
    form_class = CategoriaExamenForm
    success_url = reverse_lazy('core:categoriaexamen_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Categorías de Exámenes"
        context['title1'] = 'Ingresar Categoría de Examen'
        context['grabar'] = 'Grabar Categoría de Examen'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        categoria_examen = self.object
        save_audit(self.request, categoria_examen, action='A')
        messages.success(self.request, f"Éxito al crear la categoría {categoria_examen.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class CategoriaExamenUpdateView(UpdateView):
    model = CategoriaExamen
    template_name = 'core/categoria_examen/form.html'
    form_class = CategoriaExamenForm
    success_url = reverse_lazy('core:categoriaexamen_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Categorías de Exámenes"
        context['title1'] = 'Modificar Categoría de Examen'
        context['grabar'] = 'Actualizar Categoría de Examen'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        categoria_examen = self.object
        save_audit(self.request, categoria_examen, action='M')
        messages.success(self.request, f"Éxito al modificar la categoría {categoria_examen.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class CategoriaExamenDeleteView(DeleteView):
    model = CategoriaExamen
    success_url = reverse_lazy('core:categoriaexamen_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Categorías de Exámenes"
        context['grabar'] = 'Eliminar Categoría de Examen'
        context['description'] = f"¿Desea eliminar la categoría: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar la categoría {self.object.nombre}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class CategoriaExamenDetailView(DetailView):
    model = CategoriaExamen

    def get(self, request, *args, **kwargs):
        categoria_examen = self.get_object()
        data = {
            'id': categoria_examen.id,
            'nombre': categoria_examen.nombre,
            'descripcion': categoria_examen.descripcion,
        }
        return JsonResponse(data)
