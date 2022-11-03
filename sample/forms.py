from django import forms
from django.db import models
from .models import User

# Form用のモデル


class UserForm(forms.ModelForm):
    class Meta:
        model: models.Model = User
        fields: tuple = ('username', 'email', 'password')
        widgets: dict = {'password': forms.PasswordInput()}
