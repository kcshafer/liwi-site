from django import forms
from registration.models import User


class CustomerRegistration(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    #TODO: not sure if having a hidden field is the ideal way to do this
    is_artist = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput)
    is_active = forms.BooleanField(initial=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class SellerRegistration(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    is_artist = forms.BooleanField(initial=True, required=False, widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
