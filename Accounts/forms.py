from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        field = ('birthday', 'profile picture', 'banner image',
                'first name', 'last name', 'phone number', 
                'occupation', 'username', 'email', 'bio'
                )
class UserMutateFrom(UserChangeForm):
    class Meta:
        model = User
        field = ('birthday', 'profile picture', 'banner image',
                'first name', 'last name', 'phone number', 
                'occupation', 'username', 'email', 'bio'
                )