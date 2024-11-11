from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.attention.models import CitaMedica
from aplication.attention.forms.cita_medica import CitaMedicaForm
from doctor.utils import save_audit
from django.db.models import Q

class CitaMedicaListView(ListView):
    template_name = "attention/cita_medica/list.html"
    model = CitaMedica
    context_object_name = 'citas_medicas'
    paginate_by = 10

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query.add(Q(paciente__nombre__icontains=q) | Q(fecha__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('fecha', 'hora_cita')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Gestión de Citas Médicas"
        context['title1'] = "Consulta de Citas"
        return context

class CitaMedicaCreateView(CreateView):
    model = CitaMedica
    template_name = 'attention/cita_medica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('attention:citamedica_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Citas Médicas"
        context['title1'] = 'Registrar Nueva Cita Médica'
        context['grabar'] = 'Registrar Cita'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        cita = self.object
        save_audit(self.request, cita, action='A')
        messages.success(self.request, f"Éxito al crear la cita para {cita.paciente}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class CitaMedicaUpdateView(UpdateView):
    model = CitaMedica
    template_name = 'attention/cita_medica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('attention:citamedica_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Citas Médicas"
        context['title1'] = 'Modificar Cita Médica'
        context['grabar'] = 'Actualizar Cita'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        cita = self.object
        save_audit(self.request, cita, action='M')
        messages.success(self.request, f"Éxito al modificar la cita para {cita.paciente}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class CitaMedicaDeleteView(DeleteView):
    model = CitaMedica
    success_url = reverse_lazy('attention:citamedica_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Gestión de Citas Médicas"
        context['grabar'] = 'Eliminar Cita Médica'
        context['description'] = f"¿Desea eliminar la cita de {self.object.paciente} el {self.object.fecha} a las {self.object.hora_cita}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar la cita para {self.object.paciente}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class CitaMedicaDetailView(DetailView):
    model = CitaMedica

    def get(self, request, *args, **kwargs):
        cita = self.get_object()
        data = {
            'id': cita.id,
            'paciente': cita.paciente.nombre,
            'fecha': cita.fecha,
            'hora_cita': cita.hora_cita,
            'estado': cita.get_estado_display(),
        }
        return JsonResponse(data)
