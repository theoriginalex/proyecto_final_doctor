from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.models import Diagnostico
from aplication.core.forms.diagnostico import DiagnosticoForm
from doctor.utils import save_audit
from django.db.models import Q

class DiagnosticoListView(ListView):
    template_name = "core/diagnostico/list.html"
    model = Diagnostico
    context_object_name = 'diagnosticos'
    paginate_by = 10

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query.add(Q(codigo__icontains=q) | Q(descripcion__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('codigo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SaludSync"
        context['title1'] = "Consulta de Diagnósticos"
        return context

class DiagnosticoCreateView(CreateView):
    model = Diagnostico
    template_name = 'core/diagnostico/form.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnostico_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Ingresar Diagnóstico'
        context['grabar'] = 'Grabar Diagnóstico'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        diagnostico = self.object
        save_audit(self.request, diagnostico, action='A')
        messages.success(self.request, f"Éxito al crear el diagnóstico {diagnostico.codigo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class DiagnosticoUpdateView(UpdateView):
    model = Diagnostico
    template_name = 'core/diagnostico/form.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnostico_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Modificar Diagnóstico'
        context['grabar'] = 'Actualizar Diagnóstico'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        diagnostico = self.object
        save_audit(self.request, diagnostico, action='M')
        messages.success(self.request, f"Éxito al modificar el diagnóstico {diagnostico.codigo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class DiagnosticoDeleteView(DeleteView):
    model = Diagnostico
    success_url = reverse_lazy('core:diagnostico_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['grabar'] = 'Eliminar Diagnóstico'
        context['description'] = f"¿Desea eliminar el diagnóstico: {self.object.codigo}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el diagnóstico {self.object.codigo}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class DiagnosticoDetailView(DetailView):
    model = Diagnostico

    def get(self, request, *args, **kwargs):
        diagnostico = self.get_object()
        data = {
            'id': diagnostico.id,
            'codigo': diagnostico.codigo,
            'descripcion': diagnostico.descripcion,
            'datos_adicionales': diagnostico.datos_adicionales,
            'activo': diagnostico.activo,
        }
        return JsonResponse(data)