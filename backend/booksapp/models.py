from django.db import models

class Books(models.Model):
    isbn = models.TextField()
    book_title = models.TextField()
    book_author = models.TextField()
    year_of_publication = models.TextField()
    publisher = models.TextField()
    image_url_s = models.URLField(max_length=1000)
    image_url_m = models.URLField(max_length=1000)
    image_url_l = models.URLField(max_length=1000)

    def __str__(self):
        return self.book_title
