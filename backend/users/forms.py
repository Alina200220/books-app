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
    book = forms.CharField(max_length=100, required=False, label='Введите название книги', widget=forms.TextInput(attrs={'list': 'books'}))
    #book = forms.ModelChoiceField(queryset=Books.objects.none(), required=False, label='Выберите книгу из списка') 

class BookCreationForm(forms.ModelForm):

    class Meta:
        model = Books
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book_title'].queryset = Books.objects.none()

        if 'book_title' in self.data:
            self.fields['book_title'].queryset = Books.objects.all()

        elif self.instance.pk:
            self.fields['book_title'].queryset = Books.objects.all().filter(book_title=self.instance.book_title)

    
