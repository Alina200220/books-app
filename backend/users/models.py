from django.db import models
from django.contrib.auth.models import User

from booksapp.models import Books

class Book_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='read_books')
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='read_by_users')
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    books = models.ManyToManyField(Books)

    def __str__(self):
        return f'{self.user.username} Profile'

