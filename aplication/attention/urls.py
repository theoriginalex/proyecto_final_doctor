from django.urls import path
from aplication.attention.views.horario_atencion import HorarioAtencionListView, HorarioAtencionCreateView, HorarioAtencionUpdateView, HorarioAtencionDeleteView, HorarioAtencionDetailView
from aplication.attention.views.cita_medica import CitaMedicaListView, CitaMedicaCreateView, CitaMedicaUpdateView, CitaMedicaDeleteView, CitaMedicaDetailView

app_name='attention'

urlpatterns = [
    # horario_atencion
    path('horarioatencion_list/', HorarioAtencionListView.as_view(), name='horarioatencion_list'),
    path('horarioatencion_create/', HorarioAtencionCreateView.as_view(), name='horarioatencion_create'),
    path('horarioatencion_update/<int:pk>/', HorarioAtencionUpdateView.as_view(), name='horarioatencion_update'),
    path('horarioatencion_delete/<int:pk>/', HorarioAtencionDeleteView.as_view(), name='horarioatencion_delete'),
    path('horarioatencion_detail/<int:pk>/', HorarioAtencionDetailView.as_view(), name='horarioatencion_detail'),
    
    # Cita medica
    path('citamedica_list/', CitaMedicaListView.as_view(), name='citamedica_list'),
    path('citamedica_create/', CitaMedicaCreateView.as_view(), name='citamedica_create'),
    path('citamedica_update/<int:pk>/', CitaMedicaUpdateView.as_view(), name='citamedica_update'),
    path('citamedica_delete/<int:pk>/', CitaMedicaDeleteView.as_view(), name='citamedica_delete'),
    path('citamedica_detail/<int:pk>/', CitaMedicaDetailView.as_view(), name='citamedica_detail'),

]