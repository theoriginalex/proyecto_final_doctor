from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.models import Medicamento
from aplication.core.forms.medicamento import MedicamentoForm  # Asegúrate de crear este formulario
from django.db.models import Q

class MedicamentoListView(ListView):
    template_name = "core/medicamento/list.html"
    model = Medicamento
    context_object_name = 'medicamentos'
    paginate_by = 10

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query.add(Q(nombre__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Sistema Farmacia"
        context['title1'] = "Listado de Medicamentos"
        return context

class MedicamentoCreateView(CreateView):
    model = Medicamento
    template_name = 'core/medicamento/form.html'
    form_class = MedicamentoForm  # Crear el formulario correspondiente
    success_url = reverse_lazy('core:medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Sistema Farmacia"
        context['title1'] = 'Agregar Nuevo Medicamento'
        context['grabar'] = 'Grabar Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        medicamento = self.object
        messages.success(self.request, f"Éxito al crear el medicamento {medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


class MedicamentoUpdateView(UpdateView):
    model = Medicamento
    template_name = 'core/medicamento/form.html'
    form_class = MedicamentoForm  # Crear el formulario correspondiente
    success_url = reverse_lazy('core:medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Sistema Farmacia"
        context['title1'] = 'Modificar Medicamento'
        context['grabar'] = 'Actualizar Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        medicamento = self.object
        messages.success(self.request, f"Éxito al modificar el medicamento {medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))


class MedicamentoDeleteView(DeleteView):
    model = Medicamento
    success_url = reverse_lazy('core:medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "Sistema Farmacia"
        context['grabar'] = 'Eliminar Medicamento'
        context['description'] = f"¿Desea eliminar el medicamento {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el medicamento {self.object.nombre}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)


class MedicamentoDetailView(DetailView):
    model = Medicamento
    template_name = 'core/medicamento/detail.html'  # Si decides renderizar una plantilla en lugar de un JsonResponse

    def get(self, request, *args, **kwargs):
        medicamento = self.get_object()
        
        # Preparamos los datos para la respuesta JSON
        data = {
            'id': medicamento.id,
            'nombre': medicamento.nombre,
            'descripcion': medicamento.descripcion,
            'concentracion': medicamento.concentracion,
            'cantidad': medicamento.cantidad,
            'precio': str(medicamento.precio),  # Convertimos el precio a cadena
            'comercial': medicamento.comercial,
            'activo': medicamento.activo,
            'foto_url': medicamento.foto.url if medicamento.foto else '',
            'tipo': medicamento.tipo.nombre,
            'marca':medicamento.marca_medicamento.nombre
        }
        
        return JsonResponse(data)






