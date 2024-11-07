from django import forms
from django.core.exceptions import ValidationError
from aplication.core.models import Empleado

class EmpleadoForm(forms.ModelForm):
    # Definición de la clase Meta para especificar el modelo y los campos
    class Meta:
        model = Empleado
        fields = ['nombres', 'apellidos', 'cedula', 'fecha_nacimiento', 'cargo', 'sueldo', 'direccion', 'latitud', 'longitud', 'foto', 'activo']
        
        # Personalización de los widgets para cada campo en el formulario
        widgets = {
            'nombres': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del empleado',
                    'id': 'id_nombres',
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese el apellido del empleado',
                    'id': 'id_apellidos',
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                }
            ),
            'cedula': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese la cédula del empleado',
                    'id': 'id_cedula',
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                }
            ),
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'placeholder': 'Seleccione la fecha de nacimiento',
                    'id': 'id_fecha_nacimiento',
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                    'type': 'date',
                }
            ),
            'cargo': forms.Select(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                }
            ),
            'sueldo': forms.NumberInput(
                attrs={
                    'placeholder': 'Ingrese el sueldo del empleado',
                    'id': 'id_sueldo',
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese la dirección del empleado',
                    'id': 'id_direccion',
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                }
            ),
            'latitud': forms.NumberInput(
                attrs={
                    'placeholder': 'Ingrese la latitud',
                    'id': 'id_latitud',
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                }
            ),
            'longitud': forms.NumberInput(
                attrs={
                    'placeholder': 'Ingrese la longitud',
                    'id': 'id_longitud',
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                }
            ),
            'foto': forms.ClearableFileInput(
                attrs={
                    'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light',
                }
            ),
            'activo': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }
    
    # Validación para cédula
    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")
        if not cedula.isdigit() or len(cedula) != 10:
            raise ValidationError("La cédula debe tener 10 dígitos numéricos.")
        return cedula
    
    # Validación para el sueldo
    def clean_sueldo(self):
        sueldo = self.cleaned_data.get("sueldo")
        if sueldo <= 0:
            raise ValidationError("El sueldo debe ser mayor a 0.")
        return sueldo
