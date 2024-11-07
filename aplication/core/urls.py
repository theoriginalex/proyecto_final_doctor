from django.urls import path
from aplication.core.views.home import HomeTemplateView
from aplication.core.views.patient import PatientCreateView, PatientDeleteView, PatientDetailView, PatientListView, PatientUpdateView
from aplication.core.views.tiposangre import TipoSangreListView, TipoSangreCreateView, TipoSangreUpdateView, TipoSangreDeleteView, TipoSangreDetailView
from aplication.core.views.especialidad import EspecialidadListView, EspecialidadCreateView, EspecialidadUpdateView, EspecialidadDeleteView, EspecialidadDetailView
from aplication.core.views.doctor import DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView, DoctorDetailView  # Importando las vistas del doctor
from aplication.core.views.cargo import CargoListView, CargoCreateView, CargoUpdateView, CargoDeleteView, CargoDetailView
from aplication.core.views.empleado import EmpleadoListView, EmpleadoCreateView, EmpleadoUpdateView, EmpleadoDeleteView, EmpleadoDetailView
from aplication.core.views.tipo_medicamento import TipoMedicamentoListView, TipoMedicamentoCreateView, TipoMedicamentoUpdateView, TipoMedicamentoDeleteView, TipoMedicamentoDetailView



app_name='core'

urlpatterns = [
  # ruta principal
  path('', HomeTemplateView.as_view(),name='home'),
  
  #pacientes
  path('patient_list/',PatientListView.as_view() ,name="patient_list"),
  path('patient_create/', PatientCreateView.as_view(),name="patient_create"),
  path('patient_update/<int:pk>/', PatientUpdateView.as_view(),name='patient_update'),
  path('patient_delete/<int:pk>/', PatientDeleteView.as_view(),name='patient_delete'),
  path('patient_detail/<int:pk>/', PatientDetailView.as_view(),name='patient_detail'),
  
  #tiposangre
  path('tiposangre_list/', TipoSangreListView.as_view(), name='tiposangre_list'),
  path('tiposangre_create/', TipoSangreCreateView.as_view(), name='tiposangre_create'),
  path('tiposangre_update/<int:pk>/', TipoSangreUpdateView.as_view(), name='tiposangre_update'),
  path('tiposangre_delete/<int:pk>/', TipoSangreDeleteView.as_view(), name='tiposangre_delete'),
  path('tiposangre_detail/<int:pk>/', TipoSangreDetailView.as_view(), name='tiposangre_detail'),

  #especialidad
  path('especialidad_list/', EspecialidadListView.as_view(), name='especialidad_list'),
  path('especialidad_create/', EspecialidadCreateView.as_view(), name='especialidad_create'),
  path('especialidad_update/<int:pk>/', EspecialidadUpdateView.as_view(), name='especialidad_update'),
  path('especialidad_delete/<int:pk>/', EspecialidadDeleteView.as_view(), name='especialidad_delete'),
  path('especialidad_detail/<int:pk>/', EspecialidadDetailView.as_view(), name='especialidad_detail'),
  
  #doctor
  path('doctor_list/', DoctorListView.as_view(), name='doctor_list'),  # Listado de doctores
  path('doctor_create/', DoctorCreateView.as_view(), name='doctor_create'),  # Crear nuevo doctor
  path('doctor_update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),  # Editar doctor
  path('doctor_delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),  # Eliminar doctor
  path('doctor_detail/<int:pk>/', DoctorDetailView.as_view(), name='doctor_detail'),  # Detalles de un doctor

  #cargo
  path('cargo_list/', CargoListView.as_view(), name='cargo_list'),  # Listado de cargos
  path('cargo_create/', CargoCreateView.as_view(), name='cargo_create'),  # Crear nuevo cargo
  path('cargo_update/<int:pk>/', CargoUpdateView.as_view(), name='cargo_update'),  # Editar cargo
  path('cargo_delete/<int:pk>/', CargoDeleteView.as_view(), name='cargo_delete'),  # Eliminar cargo
  path('cargo_detail/<int:pk>/', CargoDetailView.as_view(), name='cargo_detail'),  # Detalles de un cargo

  #empleado
  path('empleado_list/', EmpleadoListView.as_view(), name='empleado_list'),  # Listado de empleados
  path('empleado_create/', EmpleadoCreateView.as_view(), name='empleado_create'),  # Crear nuevo empleado
  path('empleado_update/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado_update'),  # Editar empleado
  path('empleado_delete/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado_delete'),  # Eliminar empleado
  path('empleado_detail/<int:pk>/', EmpleadoDetailView.as_view(), name='empleado_detail'),  # Detalles de un empleado

  #tipo_medicamento
  path('tipo_medicamento_list/', TipoMedicamentoListView.as_view(), name='tipo_medicamento_list'),
  path('tipo_medicamento_create/', TipoMedicamentoCreateView.as_view(), name='tipo_medicamento_create'),
  path('tipo_medicamento_update/<int:pk>/', TipoMedicamentoUpdateView.as_view(), name='tipo_medicamento_update'),
  path('tipo_medicamento_delete/<int:pk>/', TipoMedicamentoDeleteView.as_view(), name='tipo_medicamento_delete'),
  path('tipo_medicamento_detail/<int:pk>/', TipoMedicamentoDetailView.as_view(), name='tipo_medicamento_detail'),

]