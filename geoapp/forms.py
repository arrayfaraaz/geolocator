from django import forms
from django.forms import TextInput
from .models import Measurement


class MeasurementForm(forms.ModelForm):
    
    class Meta:
        model = Measurement
        fields = ("location", "destination")
        widgets = {
            
            'location': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px',
            }),

            'destination': TextInput(attrs={
                'class': 'form-control',
                'style': 'max-width: 300px',
            })
            
        }
