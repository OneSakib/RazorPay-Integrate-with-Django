from django import forms
from .models import Coffee


class CoffeeForm(forms.ModelForm):
    class Meta:
        model = Coffee
        fields = ['name', 'email', 'contact', 'address', 'amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(
                attrs={'class': 'form-control', 'type': 'tel', 'pattern': '[0-9]{10}'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10000}),
        }
