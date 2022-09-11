from django import forms

from django.forms import ModelForm    
from django.forms.widgets import DateInput

from .models import Watering

class DateInput(forms.DateInput):
    input_type = 'date'

class WateringForm(ModelForm):
  class Meta:
    model = Watering
    fields = ['date']
    widgets = {
      'date': DateInput(attrs={'type': 'date'}),
    }