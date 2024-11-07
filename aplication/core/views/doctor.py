from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.models import Doctor
from aplication.core.forms.doctor import DoctorForm  # Asegúrate de crear este formulario
from django.db.models import Q

class DoctorListView(ListView):
    template_name = "core/doctor/list.html"
    model = Doctor
    context_object_name = 'doctores'
    paginate_by = 10

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query.add(Q(nombres__icontains=q) | Q(apellidos__icontains=q) | Q(cedula__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('apellidos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SaludSync"
        context['title1'] = "Listado de Doctores"
        return context


class DoctorCreateView(CreateView):
    model = Doctor
    template_name = 'core/doctor/form.html'
    form_class = DoctorForm  # Crear el formulario correspondiente
    success_url = reverse_lazy('core:doctor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Agregar Nuevo Doctor'
        context['grabar'] = 'Grabar Doctor'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = self.object
        messages.success(self.request, f"Éxito al crear el doctor {doctor.nombre_completo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


class DoctorUpdateView(UpdateView):
    model = Doctor
    template_name = 'core/doctor/form.html'
    form_class = DoctorForm  # Crear el formulario correspondiente
    success_url = reverse_lazy('core:doctor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Modificar Doctor'
        context['grabar'] = 'Actualizar Doctor'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = self.object
        messages.success(self.request, f"Éxito al modificar el doctor {doctor.nombre_completo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


class DoctorDeleteView(DeleteView):
    model = Doctor
    success_url = reverse_lazy('core:doctor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['grabar'] = 'Eliminar Doctor'
        context['description'] = f"¿Desea eliminar al doctor {self.object.nombre_completo}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar al doctor {self.object.nombre_completo}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'  # Si decides renderizar una plantilla en lugar de un JsonResponse

    def get(self, request, *args, **kwargs):
        doctor = self.get_object()
        
        # Recogemos todas las especialidades asociadas al doctor
        especialidades = doctor.especialidad.all().values_list('nombre', flat=True)
        
        # Preparamos los datos para la respuesta JSON
        data = {
            'id': doctor.id,
            'nombre_completo': doctor.nombre_completo,
            'cedula': doctor.cedula,
            'telefono': doctor.telefonos,
            'direccion': doctor.direccion,
            'email': doctor.email,
            'horario_atencion': doctor.horario_atencion,
            'duracion_cita': doctor.duracion_cita,
            'especialidades': list(especialidades),  # Añadimos las especialidades al JSON
            'foto_url': doctor.foto.url if doctor.foto else '',
            'curriculum_url': doctor.curriculum.url if doctor.curriculum else ''
        }
        
        return JsonResponse(data)