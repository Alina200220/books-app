from django.contrib import admin

from users.models import Book_User, Profile
from booksapp.models import Books



# Register your models here.
admin.site.register(Profile)
admin.site.register(Book_User)
admin.site.register(Books)