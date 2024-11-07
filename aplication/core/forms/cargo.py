from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import Cargo

# Definición de la clase CargoForm que hereda de ModelForm
class CargoForm(ModelForm):
    # Clase interna Meta para configurar el formulario
    class Meta:
        model = Cargo
        # Campos que se mostrarán en el formulario
        fields = ["nombre", "descripcion", "activo"]

        # Personalización de los widgets o etiquetas que se van a mostrar en el formulario html
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre del cargo (ej. Médico)",
                    "id": "id_nombre",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Descripción del cargo",
                    "id": "id_descripcion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "rows": 3,
                }
            ),
        }
        labels = {
            "nombre": "Nombre del Cargo",
            "descripcion": "Descripción",
            "activo": "Activo",
        }

    # Método de limpieza para el campo nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        # Verificar si el campo tiene menos de 2 caracteres
        if not nombre or len(nombre) < 2:
            raise ValidationError("El nombre del cargo debe tener al menos 2 caracteres.")

        return nombre
