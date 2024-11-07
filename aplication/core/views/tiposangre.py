from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.models import TipoSangre
from aplication.core.forms.tiposangre import TipoSangreForm
from doctor.utils import save_audit
from django.db.models import Q

class TipoSangreListView(ListView):
    template_name = "core/tiposangre/list.html"
    model = TipoSangre
    context_object_name = 'tipos_sangre'
    paginate_by = 10

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query.add(Q(tipo__icontains=q) | Q(descripcion__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('tipo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SaludSync"
        context['title1'] = "Consulta de Tipos de Sangre"
        return context

class TipoSangreCreateView(CreateView):
    model = TipoSangre
    template_name = 'core/tiposangre/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tiposangre_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Ingresar Tipo de Sangre'
        context['grabar'] = 'Grabar Tipo de Sangre'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_sangre = self.object
        save_audit(self.request, tipo_sangre, action='A')
        messages.success(self.request, f"Éxito al crear el tipo de sangre {tipo_sangre.tipo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class TipoSangreUpdateView(UpdateView):
    model = TipoSangre
    template_name = 'core/tiposangre/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tiposangre_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Modificar Tipo de Sangre'
        context['grabar'] = 'Actualizar Tipo de Sangre'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_sangre = self.object
        save_audit(self.request, tipo_sangre, action='M')
        messages.success(self.request, f"Éxito al modificar el tipo de sangre {tipo_sangre.tipo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class TipoSangreDeleteView(DeleteView):
    model = TipoSangre
    success_url = reverse_lazy('core:tiposangre_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['grabar'] = 'Eliminar Tipo de Sangre'
        context['description'] = f"¿Desea eliminar el tipo de sangre: {self.object.tipo}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el tipo de sangre {self.object.tipo}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class TipoSangreDetailView(DetailView):
    model = TipoSangre

    def get(self, request, *args, **kwargs):
        tipo_sangre = self.get_object()
        data = {
            'id': tipo_sangre.id,
            'tipo': tipo_sangre.tipo,
            'descripcion': tipo_sangre.descripcion,
        }
        return JsonResponse(data)