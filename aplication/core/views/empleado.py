from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.models import Empleado
from aplication.core.forms.empleado import EmpleadoForm
from doctor.utils import save_audit
from django.db.models import Q

class EmpleadoListView(ListView):
    template_name = "core/empleado/list.html"
    model = Empleado
    context_object_name = 'empleados'
    paginate_by = 10

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query.add(Q(nombres__icontains=q) | Q(apellidos__icontains=q) | Q(cedula__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('apellidos', 'nombres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SaludSync"
        context['title1'] = "Consulta de Empleados"
        return context


class EmpleadoCreateView(CreateView):
    model = Empleado
    template_name = 'core/empleado/form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')

    def get_context_data(self, **kwargs):
        """
        Agrega variables contextuales adicionales al renderizar la vista.
        """
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Crear Nuevo Empleado'
        context['grabar'] = 'Guardar Empleado'
        context['back_url'] = self.success_url
        context['is_create'] = True  # Indicador si la acción es de crear
        return context

    def form_valid(self, form):
        """
        Si el formulario es válido, guarda el objeto y genera un mensaje de éxito.
        """
        empleado = form.save(commit=False)
        empleado.created_by = self.request.user  # Asignar el usuario actual (si es necesario)
        empleado.save()
        
        # Guardar auditoría
        save_audit(self.request, empleado, action='A')
        
        # Mensaje de éxito
        messages.success(self.request, f"Empleado {empleado.nombre_completo} creado con éxito.")
        
        # Redirigir a la lista de empleados
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Si el formulario no es válido, muestra un mensaje de error.
        """
        messages.error(self.request, "Ocurrió un error al enviar el formulario. Por favor, revisa los campos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """
        Redirige a la lista de empleados después de crear uno nuevo.
        """
        return self.success_url


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    template_name = 'core/empleado/form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SaludSync"
        context['title1'] = 'Modificar Empleado'
        context['grabar'] = 'Actualizar Empleado'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        empleado = self.object
        save_audit(self.request, empleado, action='M')
        messages.success(self.request, f"Éxito al modificar el empleado {empleado.nombre_completo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    success_url = reverse_lazy('core:empleado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['grabar'] = 'Eliminar Empleado'
        context['description'] = f"¿Desea eliminar el empleado: {self.object.nombre_completo}?."
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el empleado {self.object.nombre_completo}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class EmpleadoDetailView(DetailView):
    model = Empleado

    def get(self, request, *args, **kwargs):
        empleado = self.get_object()
        data = {
            'id': empleado.id,
            'nombre_completo': empleado.nombre_completo,
            'cedula': empleado.cedula,
            'fecha_nacimiento': empleado.fecha_nacimiento,
            'cargo': empleado.cargo.nombre,
            'sueldo': str(empleado.sueldo),
            'direccion': empleado.direccion,
            'latitud': empleado.latitud,
            'longitud': empleado.longitud,
            'foto_url': empleado.foto.url if empleado.foto else None
        }
        return JsonResponse(data)
