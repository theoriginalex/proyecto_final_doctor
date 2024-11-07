from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import TipoMedicamento

class TipoMedicamentoForm(ModelForm):
    class Meta:
        model = TipoMedicamento
        fields = ["nombre", "descripcion", "activo"]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre del tipo de medicamento (ej. Analgésico)",
                    "id": "id_nombre",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Descripción del tipo de medicamento",
                    "id": "id_descripcion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "rows": 3,
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "id": "id_activo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded focus:ring-blue-500 focus:border-blue-500 block dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "nombre": "Nombre del Tipo de Medicamento",
            "descripcion": "Descripción",
            "activo": "Activo",
        }

    # Método de limpieza para el campo nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if not nombre or len(nombre) < 3:
            raise ValidationError("El nombre del tipo de medicamento debe tener al menos 3 caracteres.")
        return nombre.title()
