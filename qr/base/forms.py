from django.forms import ModelForm 
from .models import Location, Character

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description']
