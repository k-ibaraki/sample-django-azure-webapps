from django import forms
from .models import User

# Form用のモデル


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {'password': forms.PasswordInput()}
