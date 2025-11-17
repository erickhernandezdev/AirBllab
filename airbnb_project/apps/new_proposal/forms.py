from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from apps.core.models import AccommodationType, ActivityType, ServiceType


class NewProposalForm(forms.Form):
    TYPE_CHOICES = [
        ('Alojamiento', 'Alojamiento'),
        ('Actividad', 'Actividad'),
        ('Servicio', 'Servicio'),
    ]

    name = forms.CharField(max_length=100, label='Nombre')
    description = forms.CharField(widget=forms.Textarea, label='Descripción')
    type = forms.ChoiceField(choices=TYPE_CHOICES, label='Tipo')
    subtype = forms.ChoiceField(choices=[], label='Subtipo')
    location = forms.CharField(max_length=100, required=False, label='Ubicación')
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Disponible desde', required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Disponible hasta', required=False)
    price = forms.DecimalField(max_digits = 20, decimal_places = 2, min_value=0, label='Precio')
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            "id": "image-input", 
            "hidden": True
        }),
        required=False, 
        label="Imagen"
    )

    def __init__(self, *args, **kwargs):
        selected_type = kwargs.pop('selected_type', None)
        super().__init__(*args, **kwargs)
        today_iso = date.today().isoformat()
        if 'start_date' in self.fields:
            self.fields['start_date'].widget.attrs.setdefault('min', today_iso)
        if 'end_date' in self.fields:
            self.fields['end_date'].widget.attrs.setdefault('min', today_iso)

        if selected_type == 'Alojamiento':
            self.fields['subtype'].choices = [(a.name, a.name) for a in AccommodationType.objects.using('airbnb_user').all()]
        elif selected_type == 'Actividad':
            self.fields['subtype'].choices = [(a.name, a.name) for a in ActivityType.objects.using('airbnb_user').all()]
        elif selected_type == 'Servicio':
            self.fields['subtype'].choices = [(s.name, s.name) for s in ServiceType.objects.using('airbnb_user').all()]
        else:
            self.fields['subtype'].choices = []

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        if start and end and end < start:
            self.add_error('end_date', 'La fecha final debe ser igual o posterior a la fecha de inicio.')
        return cleaned
