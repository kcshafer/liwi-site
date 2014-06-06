from django import forms

from art.models import Art
from registration.models import User

class ArtForm(forms.ModelForm):
    
    class Meta:
        model = Art
        fields = ('photo', 'title', 'description')
        exclude = ['user']