from django import forms
from pezInterface.models import Modulo, Jaula

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Modulo

        """moduloNumero = forms.IntegerField(
            widget=forms.TextInput(
                attrs={'class': 'form-control'}),
            label='N° de Módulo',
            required=True
        )
        moduloDescription = forms.CharField(
            widget=forms.Textarea(
                attrs={'class': 'form-control'}),
            label='Descripción',
            required=False
        )"""

        fields = [
            'moduloNumero',
            'moduloDescription',
        ]
        labels = {
            'moduloNumero': 'N° de Módulo',
            'moduloDescription': 'Descripción',
        }
        widgets = {
            'moduloNumero': forms.TextInput(attrs={'class': 'form-control'}),
            'moduloDescription': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }

class JaulaForm(forms.ModelForm):
    class Meta:
        model = Jaula

        fields = [
            'jaulaNumero',
        ]
        labels = {
            'jaulaNumero': 'N° de Jaula',
        }
        widgets = {
            'jaulaNumero': forms.TextInput(attrs={'class': 'form-control'}),
        }