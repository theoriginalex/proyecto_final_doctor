from django import forms
from aplication.core.models import Especialidad

class EspecialidadForm(forms.ModelForm):
    # Clase interna Meta para configurar el formulario
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre de la especialidad',
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción de la especialidad',
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                    'rows': 4,
                }
            ),
            'activo': forms.CheckboxInput(
                attrs={
                    'class': 'mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
                }
            ),
        }
        labels = {
            'nombre': 'Nombre de la Especialidad',
            'descripcion': 'Descripción de la Especialidad',
            'activo': '¿Está activo?',
        }

        error_messages = {
            'nombre': {
                'required': 'El nombre de la especialidad es obligatorio.',
                'max_length': 'El nombre de la especialidad no puede superar los 100 caracteres.',
            },
            'descripcion': {
                'max_length': 'La descripción no puede superar los 500 caracteres.',
            },
        }

    # Método de limpieza para el campo nombre
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return nombre.upper()

    # Método de limpieza para la descripción (opcional)
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion and len(descripcion) > 500:
            raise forms.ValidationError("La descripción no puede exceder los 500 caracteres.")
        return descripcion

