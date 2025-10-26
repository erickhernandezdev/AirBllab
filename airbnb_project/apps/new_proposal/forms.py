from datetime import date

from django import forms
from django.core.exceptions import ValidationError


class NewProposalForm(forms.Form):
    TYPE_CHOICES = [
        ('Alojamiento', 'Alojamiento'),
        ('Actividad', 'Actividad'),
        ('Servicio', 'Servicio'),
    ]

    name = forms.CharField(max_length=100, label='Nombre')
    description = forms.CharField(widget=forms.Textarea, label='Descripción')
    type = forms.ChoiceField(choices=TYPE_CHOICES, label='Tipo')
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha de inicio')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha final')
    price = forms.DecimalField(max_digits = 20, decimal_places = 2, min_value=0, label='Precio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today_iso = date.today().isoformat()
        if 'start_date' in self.fields:
            self.fields['start_date'].widget.attrs.setdefault('min', today_iso)
        if 'end_date' in self.fields:
            self.fields['end_date'].widget.attrs.setdefault('min', today_iso)

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        if start and end and end < start:
            self.add_error('end_date', 'La fecha final debe ser igual o posterior a la fecha de inicio.')
        return cleaned
