from django import forms

from art.models import Art

class ArtForm(forms.ModelForm):
    
    class Meta:
        model = Art
        fields = ('photo', 'title', 'description')
        exclude = ['user']