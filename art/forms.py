from django import forms

from art.fields import CategoryModelChoiceField
from art.models import Art, Category

class ArtForm(forms.ModelForm):

    categories = CategoryModelChoiceField(queryset=Category.objects.values('name', 'id'), 
  empty_label="     ")
    class Meta:
        model = Art
        fields = ('photo', 'title', 'description')
        exclude = ['user', 'category']

    def clean(self):
        super(ArtForm, self).clean() #if necessary
        try:
            del self._errors['categories']
        except:
            pass
            
        return self.cleaned_data  