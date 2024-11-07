from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from aplication.core.models import Especialidad
from aplication.core.forms.especialidad import EspecialidadForm  # Asegúrate de tener un formulario correspondiente
from doctor.utils import save_audit  # Si deseas realizar auditoría o alguna otra acción
from django.db.models import Q

# Lista de Especialidades
class EspecialidadListView(ListView):
    template_name = 'core/especialidad/list.html'
    model = Especialidad
    context_object_name = 'especialidades'
    paginate_by = 10  # Puedes ajustar la cantidad de resultados por página

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            # Filtrado por nombre o descripción de la especialidad
            query.add(Q(nombre__icontains=q) | Q(descripcion__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SaludSync"
        context['title1'] = "Consulta de Especialidades"
        return context

# Crear Especialidad
class EspecialidadCreateView(CreateView):
    model = Especialidad
    template_name = 'core/especialidad/form.html'
    form_class = EspecialidadForm  # Asegúrate de crear el formulario correspondiente
    success_url = reverse_lazy('core:especialidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Especialidades"
        context['title1'] = 'Crear Nueva Especialidad'
        context['grabar'] = 'Grabar Especialidad'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        especialidad = self.object
        save_audit(self.request, especialidad, action='A')
        messages.success(self.request, f"Éxito al crear la especialidad {especialidad.nombre}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


# Actualizar Especialidad
class EspecialidadUpdateView(UpdateView):
    model = Especialidad
    template_name = 'core/especialidad/form.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('core:especialidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Especialidades"
        context['title1'] = 'Modificar Especialidad'
        context['grabar'] = 'Actualizar Especialidad'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        especialidad = self.object
        save_audit(self.request, especialidad, action='M')
        messages.success(self.request, f"Éxito al modificar la especialidad {especialidad.nombre}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


# Eliminar Especialidad
class EspecialidadDeleteView(DeleteView):
    model = Especialidad
    success_url = reverse_lazy('core:especialidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Especialidades"
        context['grabar'] = 'Eliminar Especialidad'
        context['description'] = f"¿Desea eliminar la especialidad: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar la especialidad {self.object.nombre}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)


# Detalles de una Especialidad
class EspecialidadDetailView(DetailView):
    model = Especialidad

    def get(self, request, *args, **kwargs):
        especialidad = self.get_object()
        data = {
            'id': especialidad.id,
            'nombre': especialidad.nombre,
            'descripcion': especialidad.descripcion,
            'activo': especialidad.activo,
        }
        return JsonResponse(data)
