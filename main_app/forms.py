from django.forms import ModelForm
from .models import Watering

class WateringForm(ModelForm):
    class Meta:
        model = Watering
        fields = ['date']