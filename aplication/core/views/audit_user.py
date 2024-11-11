from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q
from aplication.core.models import AuditUser
from django.contrib import messages

class AuditUserListView(ListView):
    template_name = "core/audit_user/list.html"
    model = AuditUser
    context_object_name = 'auditorias_usuario'
    paginate_by = 10

    def get_queryset(self):
        query = Q()
        q = self.request.GET.get('q')
        if q:
            query.add(Q(usuario__username__icontains=q) | Q(tabla__icontains=q), Q.OR)
        return self.model.objects.filter(query).order_by('-fecha', 'hora')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "SaludSync"
        context['title1'] = "Consulta de Auditorías de Usuario"
        return context


class AuditUserDetailView(DetailView):
    model = AuditUser

    def get(self, request, *args, **kwargs):
        audit_user = self.get_object()
        data = {
            'id': audit_user.id,
            'usuario': audit_user.usuario.username,
            'tabla': audit_user.tabla,
            'registroid': audit_user.registroid,
            'accion': audit_user.accion,
            'fecha': audit_user.fecha,
            'hora': audit_user.hora,
            'estacion': audit_user.estacion,
        }
        return JsonResponse(data)
