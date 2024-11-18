from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from users.models import Book_User, Profile
from .models import Books
from ajax_select.fields import AutoCompleteSelectMultipleField
from django_select2 import forms as s2forms
from crispy_forms.helper import FormHelper

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# forms.py

class BookForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Введите название книги')
    book = forms.ModelChoiceField(queryset=Books.objects.none(), required=False, label='Выберите книгу из списка') 

    
