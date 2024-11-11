from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from aplication.core.models import TipoCategoria
from aplication.core.forms.tipo_categoria import TipoCategoriaForm
from doctor.utils import save_audit
from django.db.models import Q

class TipoCategoriaListView(ListView):
    template_name = "core/tipo_categoria/list.html"
    model = TipoCategoria
    context_object_name = 'tipos_categoria'
    paginate_by = 10

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query.add(Q(nombre__icontains=q) | Q(descripcion__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('categoria_examen', 'nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SaludSync"
        context['title1'] = "Consulta de Tipos de Categoría de Examen"
        return context

class TipoCategoriaCreateView(CreateView):
    model = TipoCategoria
    template_name = 'core/tipo_categoria/form.html'
    form_class = TipoCategoriaForm
    success_url = reverse_lazy('core:tipocategoria_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Ingresar Tipo de Categoría de Examen'
        context['grabar'] = 'Grabar Tipo de Categoría'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_categoria = self.object
        save_audit(self.request, tipo_categoria, action='A')
        messages.success(self.request, f"Éxito al crear el tipo de categoría {tipo_categoria.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class TipoCategoriaUpdateView(UpdateView):
    model = TipoCategoria
    template_name = 'core/tipo_categoria/form.html'
    form_class = TipoCategoriaForm
    success_url = reverse_lazy('core:tipocategoria_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['title1'] = 'Modificar Tipo de Categoría de Examen'
        context['grabar'] = 'Actualizar Tipo de Categoría'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_categoria = self.object
        save_audit(self.request, tipo_categoria, action='M')
        messages.success(self.request, f"Éxito al modificar el tipo de categoría {tipo_categoria.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class TipoCategoriaDeleteView(DeleteView):
    model = TipoCategoria
    success_url = reverse_lazy('core:tipocategoria_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = "SaludSync"
        context['grabar'] = 'Eliminar Tipo de Categoría de Examen'
        context['description'] = f"¿Desea eliminar el tipo de categoría: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el tipo de categoría {self.object.nombre}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class TipoCategoriaDetailView(DetailView):
    model = TipoCategoria

    def get(self, request, *args, **kwargs):
        tipo_categoria = self.get_object()
        data = {
            'id': tipo_categoria.id,
            'nombre': tipo_categoria.nombre,
            'descripcion': tipo_categoria.descripcion,
            'valor_minimo': tipo_categoria.valor_minimo,
            'valor_maximo': tipo_categoria.valor_maximo,
            'activo': tipo_categoria.activo,
            'categoria': tipo_categoria.categoria_examen.nombre,
        }
        return JsonResponse(data)
