from django import forms

class NewProposalForm(forms.Form):
    TYPE_CHOICES = [
        ('alojamiento', 'Alojamiento'),
        ('actividad', 'Actividad'),
        ('servicio', 'Servicio'),
    ]

    id = forms.IntegerField(min_value=0, max_value=999999999, label='id')
    name = forms.CharField(max_length=100, label='name')
    description = forms.CharField(widget=forms.Textarea, label='description')
    type = forms.ChoiceField(choices=TYPE_CHOICES, label='Type')
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='start_date')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='end_date')
    price = forms.DecimalField(max_digits = 10, decimal_places = 2, min_value=0, label='price')
