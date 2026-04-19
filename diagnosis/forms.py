from django import forms
from .models import Diagnosis

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['patient_name', 'patient_age', 'patient_gender', 
                  'clinical_notes', 'xray_image']
        widgets = {
            'patient_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom complet du patient'
            }),
            'patient_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Âge'
            }),
            'patient_gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'clinical_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Symptômes, antécédents, observations cliniques...'
            }),
            'xray_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }