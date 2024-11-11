from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import TipoCategoria

class TipoCategoriaForm(ModelForm):
    class Meta:
        model = TipoCategoria
        fields = ["categoria_examen", "nombre", "descripcion", "valor_minimo", "valor_maximo", "activo"]
        
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre del examen (ej. Colesterol)",
                    "id": "id_nombre",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Descripción del examen",
                    "id": "id_descripcion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "rows": 3,
                }
            ),
            "valor_minimo": forms.TextInput(
                attrs={
                    "placeholder": "Valor mínimo (ej. 70 mg/dL)",
                    "id": "id_valor_minimo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "valor_maximo": forms.TextInput(
                attrs={
                    "placeholder": "Valor máximo (ej. 100 mg/dL)",
                    "id": "id_valor_maximo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "id": "id_activo",
                    "class": "bg-blue-500 border-gray-300 text-white rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
        }

        labels = {
            "categoria_examen": "Categoría del Examen",
            "nombre": "Nombre del Examen",
            "descripcion": "Descripción",
            "valor_minimo": "Valor Mínimo",
            "valor_maximo": "Valor Máximo",
            "activo": "Activo",
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if not nombre or len(nombre) < 2:
            raise ValidationError("El nombre del examen debe tener al menos 2 caracteres.")
        return nombre.title()

    def clean_valor_minimo(self):
        valor_minimo = self.cleaned_data.get("valor_minimo")
        if valor_minimo and not valor_minimo.replace('.', '', 1).isdigit():
            raise ValidationError("El valor mínimo debe ser un número.")
        return valor_minimo

    def clean_valor_maximo(self):
        valor_maximo = self.cleaned_data.get("valor_maximo")
        if valor_maximo and not valor_maximo.replace('.', '', 1).isdigit():
            raise ValidationError("El valor máximo debe ser un número.")
        return valor_maximo
