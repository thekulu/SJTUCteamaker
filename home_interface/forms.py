from django import forms
from django.contrib.auth.models import User
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name' ,'user_id','user_password','bio', 'major']

