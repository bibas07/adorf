from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Username already exits")
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['username','email','password1','password2']