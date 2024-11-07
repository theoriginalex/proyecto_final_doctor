from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import Doctor

class DoctorForm(ModelForm):
    # Clase interna Meta para configurar el formulario
    class Meta:
        model = Doctor
        # Campos que se mostrarán en el formulario
        fields = [
            "nombres", 
            "apellidos", 
            "cedula", 
            "fecha_nacimiento", 
            "direccion", 
            "latitud", 
            "longitud", 
            "codigoUnicoDoctor", 
            "especialidad", 
            "telefonos", 
            "email", 
            "horario_atencion", 
            "duracion_cita", 
            "curriculum", 
            "firmaDigital", 
            "foto", 
            "imagen_receta", 
            "activo"
        ]

        # Personalización de los widgets o etiquetas que se van a mostrar en el formulario html
        widgets = {
            "nombres": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese los nombres del doctor",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "apellidos": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese los apellidos del doctor",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "cedula": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese la cédula del doctor",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "fecha_nacimiento": forms.DateInput(
                attrs={
                    "placeholder": "Seleccione la fecha de nacimiento",
                    "type": "date",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "direccion": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese la dirección del trabajo del doctor",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "telefonos": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese los teléfonos del doctor",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Ingrese el correo electrónico del doctor",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "horario_atencion": forms.Textarea(
                attrs={
                    "placeholder": "Ingrese el horario de atención del doctor",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                    "rows": 3,
                }
            ),
            "curriculum": forms.ClearableFileInput(
                attrs={
                    "class": "block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white",
                }
            ),
            "firmaDigital": forms.ClearableFileInput(
                attrs={
                    "class": "block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white",
                }
            ),
            "foto": forms.ClearableFileInput(
                attrs={
                    "class": "block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white",
                }
            ),
            "imagen_receta": forms.ClearableFileInput(
                attrs={
                    "class": "block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white",
                }
            ),
        }

        labels = {
            "nombres": "Nombres del Doctor",
            "apellidos": "Apellidos del Doctor",
            "cedula": "Cédula",
            "fecha_nacimiento": "Fecha de Nacimiento",
            "direccion": "Dirección de Trabajo",
            "latitud": "Latitud",
            "longitud": "Longitud",
            "codigoUnicoDoctor": "Código Único del Doctor",
            "especialidad": "Especialidades",
            "telefonos": "Teléfonos",
            "email": "Correo Electrónico",
            "horario_atencion": "Horario de Atención",
            "duracion_cita": "Duración de la Cita (minutos)",
            "curriculum": "Curriculum Vitae",
            "firmaDigital": "Firma Digital",
            "foto": "Foto del Doctor",
            "imagen_receta": "Imagen para Recetas",
            "activo": "Activo",
        }

    # Método de limpieza para el campo cédula
    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")
        # Verificar si la cédula tiene 10 caracteres
        if len(cedula) != 10:
            raise ValidationError("La cédula debe tener exactamente 10 caracteres.")
        return cedula

    # Método de limpieza para el campo latitud
    def clean_latitud(self):
        latitud = self.cleaned_data.get("latitud")
        # Validar si la latitud está en el rango adecuado
        if latitud and (latitud < -90 or latitud > 90):
            raise ValidationError("La latitud debe estar entre -90 y 90 grados.")
        return latitud

    # Método de limpieza para el campo longitud
    def clean_longitud(self):
        longitud = self.cleaned_data.get("longitud")
        # Validar si la longitud está en el rango adecuado
        if longitud and (longitud < -180 or longitud > 180):
            raise ValidationError("La longitud debe estar entre -180 y 180 grados.")
        return longitud
