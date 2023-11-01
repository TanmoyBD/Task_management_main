from django import forms
from .models import CustomUser
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Replace 'User' with your user model if needed
        fields = ['username','email', 'password1', 'password2']

    
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    
    
# forms.py

from django import forms

class ConfirmationForm(forms.Form):
    confirmation_code = forms.CharField(label='Confirmation Code', max_length=6, widget=forms.TextInput(attrs={'autocomplete': 'off'}))




from django import forms

class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
