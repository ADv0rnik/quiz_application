from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from profile.models import Student
from django.forms import TextInput, EmailInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'date_created']
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control rounded-4",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
            }),
            'last_name': TextInput(attrs={
                'class': "form-control rounded-4",
                'style': 'max-width: 300px;',
                'placeholder': 'Surname'
            }),
            'mail': EmailInput(attrs={
                'class': "form-control rounded-4",
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
            }),
            'department': TextInput(attrs={
                'class': "form-control rounded-4",
                'style': 'max-width: 300px;',
                'placeholder': 'Department'
            }),
            'occupation': TextInput(attrs={
                'class': "form-control rounded-4",
                'style': 'max-width: 300px;',
                'placeholder': 'Occupation'
            })
        }
