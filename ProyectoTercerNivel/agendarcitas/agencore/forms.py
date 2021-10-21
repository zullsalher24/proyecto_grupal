from django import forms

from .models import *


class Contactform(forms.Form):
    name = forms.CharField(label="Nombre", required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe su Nombre'}),
                           min_length=3, max_length=100)
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Escribe su Email'}), min_length=3, max_length=100)
    content = forms.CharField(label="Contenido", required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escribe tu mensaje'}), min_length=10,
                              max_length=1000)


class Pacienteform(forms.ModelForm):
    class Meta:
        model = paciente
        fields = ['pacientecedula',
                  'pacienteapellido',
                  'pacientenombre',
                  'pacientedireccion',
                  'pacienteestado',
                  ]

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'edad', 'direccion', 'cedula', 'correo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        # self.fields['apellido'].widget.attrs.update({'class': 'form-control'})
        self.fields['apellido'].widget.attrs.update(size='80')


class ValoresForm(forms.Form):
    valor1 = forms.IntegerField()
    valor2 = forms.IntegerField()
    total = forms.IntegerField()

class Doctorform(forms.ModelForm):
    class Meta:
        model = doctor
        fields = ['doctorcedula']



