from django import forms
from django.forms import ModelForm, ValidationError
from aplication.core.models import Medicamento

class MedicamentoForm(ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            "tipo", 
            "marca_medicamento", 
            "nombre", 
            "descripcion", 
            "concentracion", 
            "cantidad", 
            "precio", 
            "comercial", 
            "activo", 
            "foto"
        ]

        # Personalización de los widgets o etiquetas que se van a mostrar en el formulario HTML
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre del medicamento",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Descripción del medicamento",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                    "rows": 3,
                }
            ),
            "concentracion": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese la concentración del medicamento",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "cantidad": forms.NumberInput(
                attrs={
                    "placeholder": "Ingrese la cantidad disponible",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "precio": forms.NumberInput(
                attrs={
                    "placeholder": "Ingrese el precio del medicamento",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "foto": forms.FileInput(
                attrs={
                    "type": "file",
                    "id": "id_foto",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }

        labels = {
            "tipo": "Tipo de Medicamento",
            "marca_medicamento": "Marca del Medicamento",
            "nombre": "Nombre del Medicamento",
            "descripcion": "Descripción",
            "concentracion": "Concentración",
            "cantidad": "Cantidad",
            "precio": "Precio",
            "comercial": "Es Comercial",
            "activo": "Activo",
            "foto": "Foto del Medicamento",
        }

    # Método de limpieza para el campo nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        # Verificar si el nombre tiene más de 100 caracteres
        if len(nombre) > 100:
            raise ValidationError("El nombre del medicamento no puede exceder los 100 caracteres.")
        return nombre

    # Método de limpieza para el campo precio
    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        # Verificar si el precio es mayor a 0
        if precio <= 0:
            raise ValidationError("El precio debe ser mayor que 0.")
        return precio


