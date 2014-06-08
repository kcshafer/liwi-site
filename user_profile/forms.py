from django import forms
from user_profile.models import Profile


class MyProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('photo', 'bio', 'twitter')