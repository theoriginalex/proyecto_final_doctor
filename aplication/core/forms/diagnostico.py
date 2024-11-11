from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import Diagnostico

class DiagnosticoForm(ModelForm):
    class Meta:
        model = Diagnostico
        fields = ["codigo", "descripcion", "datos_adicionales", "activo"]

        widgets = {
            "codigo": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el código del diagnóstico (ej. CIE-10)",
                    "id": "id_codigo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.TextInput(
                attrs={
                    "placeholder": "Descripción del diagnóstico",
                    "id": "id_descripcion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "datos_adicionales": forms.Textarea(
                attrs={
                    "placeholder": "Información adicional relevante",
                    "id": "id_datos_adicionales",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "rows": 4,
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "class": "form-checkbox h-4 w-4 text-blue-600 transition duration-150 ease-in-out",
                }
            ),
        }
        labels = {
            "codigo": "Código del Diagnóstico",
            "descripcion": "Descripción",
            "datos_adicionales": "Datos Adicionales",
            "activo": "Activo",
        }

    def clean_codigo(self):
        codigo = self.cleaned_data.get("codigo")
        if not codigo or len(codigo) < 3:
            raise ValidationError("El código debe tener al menos 3 caracteres.")
        return codigo.upper()
