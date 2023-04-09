from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


'''Updating the contents of the User'''


class UserUpdateForm(forms.ModelForm):
    # Additional fields
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


'''Updating the contents of the Profile'''


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
