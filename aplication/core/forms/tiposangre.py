from django.forms import ModelForm, ValidationError
from django import forms

from aplication.core.models import TipoSangre

# Definición de la clase TipoSangreForm que hereda de ModelForm
class TipoSangreForm(ModelForm):
    # Clase interna Meta para configurar el formulario
    class Meta:
        model = TipoSangre
        # Campos que se mostrarán en el formulario
        fields = ["tipo", "descripcion"]

        # Personalización de los widgets o etiquetas que se van a mostrar en el formulario html
        widgets = {
            "tipo": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el tipo de sangre (ej. A+)",
                    "id": "id_tipo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Descripción del tipo de sangre",
                    "id": "id_descripcion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "rows": 3,
                }
            ),
        }
        labels = {
            "tipo": "Tipo de Sangre",
            "descripcion": "Descripción",
        }

    # Método de limpieza para el campo tipo
    def clean_tipo(self):
        tipo = self.cleaned_data.get("tipo")
        # Verificar si el campo tiene menos de 2 caracteres
        if not tipo or len(tipo) < 2:
            raise ValidationError("El tipo de sangre debe tener al menos 2 caracteres.")

        return tipo.upper()
