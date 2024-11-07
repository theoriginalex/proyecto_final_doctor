from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.models import TipoMedicamento
from aplication.core.forms.tipo_medicamento import TipoMedicamentoForm
from doctor.utils import save_audit
from django.db.models import Q

class TipoMedicamentoListView(ListView):
    template_name = "core/tipo_medicamento/list.html"
    model = TipoMedicamento
    context_object_name = 'tipos_medicamento'
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
        context['title1'] = "Consulta de Tipos de Medicamento"
        return context

class TipoMedicamentoCreateView(CreateView):
    model = TipoMedicamento
    template_name = 'core/tipo_medicamento/form.html'
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy('core:tipo_medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Ingresar Tipo de Medicamento'
        context['grabar'] = 'Grabar Tipo de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_medicamento = self.object
        save_audit(self.request, tipo_medicamento, action='A')
        messages.success(self.request, f"Éxito al crear el tipo de medicamento {tipo_medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class TipoMedicamentoUpdateView(UpdateView):
    model = TipoMedicamento
    template_name = 'core/tipo_medicamento/form.html'
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy('core:tipo_medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SaludSync"
        context['title1'] = 'Modificar Tipo de Medicamento'
        context['grabar'] = 'Actualizar Tipo de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_medicamento = self.object
        save_audit(self.request, tipo_medicamento, action='M')
        messages.success(self.request, f"Éxito al modificar el tipo de medicamento {tipo_medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class TipoMedicamentoDeleteView(DeleteView):
    model = TipoMedicamento
    success_url = reverse_lazy('core:tipo_medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['grabar'] = 'Eliminar Tipo de Medicamento'
        context['description'] = f"¿Desea eliminar el tipo de medicamento: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el tipo de medicamento {self.object.nombre}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class TipoMedicamentoDetailView(DetailView):
    model = TipoMedicamento

    def get(self, request, *args, **kwargs):
        tipo_medicamento = self.get_object()
        data = {
            'id': tipo_medicamento.id,
            'nombre': tipo_medicamento.nombre,
            'descripcion': tipo_medicamento.descripcion,
        }
        return JsonResponse(data)
