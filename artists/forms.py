from django import forms
from django.contrib.admin import widgets

from artists.models import FeaturedArtist


class FeaturedArtistForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class':'date_field'}), required=True)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'date_field'}), required=True)

    class Meta:
        model = FeaturedArtist
        fields = ('start_date', 'end_date')


    def clean(self):
        cleaned_data = super(FeaturedArtistForm, self).clean() #if necessary

        start_date = cleaned_data.get('start_date', None)
        end_date = cleaned_data.get('end_date', None)
        if start_date and end_date:
            if(start_date > end_date):
                del cleaned_data['start_date']
                self._errors["start_date"] = self.error_class(['Start date cannot be greater than end date.'])

        return cleaned_data