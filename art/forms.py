from django import forms

from art.fields import CategoryModelChoiceField, TagModelMultipleChoiceField
from art.models import Art, Category, Tag

class ArtForm(forms.ModelForm):

    categories = CategoryModelChoiceField(queryset=Category.objects.values('name', 'id'))
    tags = TagModelMultipleChoiceField(queryset=Tag.objects.all().values_list('name', 'id'))

    class Meta:
        model = Art
        fields = ('photo', 'title', 'description')
        exclude = ['user', 'category']

    def clean(self):
        super(ArtForm, self).clean() #if necessary
        try:
            del self._errors['categories']
            #del self._errors['tags']
        except:
            pass
            
        return self.cleaned_data  