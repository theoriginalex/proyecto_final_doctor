import datetime
from django.forms import ModelForm, ValidationError
from django import forms
from aplication.attention.models import CitaMedica

class CitaMedicaForm(ModelForm):
    class Meta:
        model = CitaMedica
        fields = ["paciente", "fecha", "hora_cita", "estado"]

        widgets = {
            "paciente": forms.Select(
                attrs={
                    "class": "form-select shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "fecha": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "hora_cita": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "estado": forms.Select(
                attrs={
                    "class": "form-select shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "paciente": "Paciente",
            "fecha": "Fecha de la Cita",
            "hora_cita": "Hora de la Cita",
            "estado": "Estado de la Cita",
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        if fecha and fecha < datetime.date.today():
            raise ValidationError("La fecha de la cita no puede ser en el pasado.")
        return fecha

    def clean_hora_cita(self):
        hora_cita = self.cleaned_data.get("hora_cita")
        if hora_cita and (hora_cita.hour < 8 or hora_cita.hour > 18):
            raise ValidationError("La hora de la cita debe estar entre las 08:00 y 18:00.")
        return hora_cita
