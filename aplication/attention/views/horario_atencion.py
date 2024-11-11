from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.attention.models import HorarioAtencion
from aplication.attention.forms.horario_atencion import HorarioAtencionForm
from doctor.utils import save_audit
from django.db.models import Q

class HorarioAtencionListView(ListView):
    template_name = "attention/horario_atencion/list.html"
    model = HorarioAtencion
    context_object_name = 'horarios_atencion'
    paginate_by = 10

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query.add(Q(dia_semana__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('dia_semana')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SaludSync"
        context['title1'] = "Consulta de Horarios de Atención"
        return context

class HorarioAtencionCreateView(CreateView):
    model = HorarioAtencion
    template_name = 'attention/horario_atencion/form.html'
    form_class = HorarioAtencionForm
    success_url = reverse_lazy('attention:horarioatencion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Ingresar Horario de Atención'
        context['grabar'] = 'Grabar Horario de Atención'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        horario_atencion = self.object
        save_audit(self.request, horario_atencion, action='A')
        messages.success(self.request, f"Éxito al crear el horario de atención para el día {horario_atencion.dia_semana}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class HorarioAtencionUpdateView(UpdateView):
    model = HorarioAtencion
    template_name = 'attention/horario_atencion/form.html'
    form_class = HorarioAtencionForm
    success_url = reverse_lazy('attention:horarioatencion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Modificar Horario de Atención'
        context['grabar'] = 'Actualizar Horario de Atención'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        horario_atencion = self.object
        save_audit(self.request, horario_atencion, action='M')
        messages.success(self.request, f"Éxito al modificar el horario de atención para el día {horario_atencion.dia_semana}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class HorarioAtencionDeleteView(DeleteView):
    model = HorarioAtencion
    success_url = reverse_lazy('attention:horarioatencion_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['grabar'] = 'Eliminar Horario de Atención'
        context['description'] = f"¿Desea eliminar el horario de atención para el día: {self.object.dia_semana}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el horario de atención para el día {self.object.dia_semana}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class HorarioAtencionDetailView(DetailView):
    model = HorarioAtencion

    def get(self, request, *args, **kwargs):
        horario_atencion = self.get_object()
        data = {
            'id': horario_atencion.id,
            'dia_semana': horario_atencion.dia_semana,
            'hora_inicio': horario_atencion.hora_inicio,
            'hora_fin': horario_atencion.hora_fin,
            'Intervalo_desde': horario_atencion.Intervalo_desde,
            'Intervalo_hasta': horario_atencion.Intervalo_hasta,
            'activo': horario_atencion.activo,
        }
        return JsonResponse(data)
