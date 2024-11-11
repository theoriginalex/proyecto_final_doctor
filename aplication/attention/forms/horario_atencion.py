from django.forms import ModelForm, ValidationError
from django import forms
from aplication.attention.models import HorarioAtencion

class HorarioAtencionForm(ModelForm):
    class Meta:
        model = HorarioAtencion
        fields = ["dia_semana", "hora_inicio", "hora_fin", "Intervalo_desde", "Intervalo_hasta", "activo"]
        
        widgets = {
            "dia_semana": forms.Select(
                attrs={
                    "id": "id_dia_semana",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "hora_inicio": forms.TimeInput(
                attrs={
                    "type": "time",
                    "id": "id_hora_inicio",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "hora_fin": forms.TimeInput(
                attrs={
                    "type": "time",
                    "id": "id_hora_fin",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "Intervalo_desde": forms.TimeInput(
                attrs={
                    "type": "time",
                    "id": "id_intervalo_desde",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "Intervalo_hasta": forms.TimeInput(
                attrs={
                    "type": "time",
                    "id": "id_intervalo_hasta",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "id": "id_activo",
                    "class": "focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded dark:bg-principal dark:border-gray-600 dark:focus:ring-blue-500 dark:focus:border-blue-500",
                }
            ),
        }
        labels = {
            "dia_semana": "Día de la Semana",
            "hora_inicio": "Hora de Inicio",
            "hora_fin": "Hora de Fin",
            "Intervalo_desde": "Intervalo desde",
            "Intervalo_hasta": "Intervalo hasta",
            "activo": "Activo",
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")
        intervalo_desde = cleaned_data.get("Intervalo_desde")
        intervalo_hasta = cleaned_data.get("Intervalo_hasta")
        
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
        
        if intervalo_desde and intervalo_hasta:
            if intervalo_desde >= intervalo_hasta:
                raise ValidationError("El intervalo de descanso debe tener una hora de fin posterior a la de inicio.")
        
        return cleaned_data
