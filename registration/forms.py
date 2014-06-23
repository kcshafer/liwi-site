from django import forms

from registration.fields import QuestionModelChoiceField
from registration.models import User, SecurityQuestion


class CustomerRegistration(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    #TODO: not sure if having a hidden field is the ideal way to do this
    is_artist = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput)
    secret_question = QuestionModelChoiceField(queryset=SecurityQuestion.objects.all().values('question', 'id'), required=False)
    secret_answer = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super(CustomerRegistration, self).clean() #if necessary
        email = cleaned_data.get('email')
        if User.objects.all().filter(email=email):
            self._errors["email"] = self.error_class(['This email is already registered.'])
            del cleaned_data['email']

        try:
            del self._errors['secret_question']
        except:
            pass

        return cleaned_data

class SellerRegistration(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    is_artist = forms.BooleanField(initial=True, required=False, widget=forms.HiddenInput)
    secret_question = QuestionModelChoiceField(queryset=SecurityQuestion.objects.all().values('question', 'id'), required=False)
    secret_answer = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def clean(self):
            cleaned_data = super(SellerRegistration, self).clean() #if necessary
            email = cleaned_data.get('email')
            if User.objects.all().filter(email=email):
                self._errors["email"] = self.error_class(['This email is already registered.'])
                del cleaned_data['email']

            try:
                del self._errors['secret_question']
            except:
                pass
                
            return cleaned_data

class AccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('city', 'state', 'email')