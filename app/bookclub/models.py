"""from django.db import models

class Tutorial(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    tutorial_url = models.CharField(max_length=200, blank=False, default='')
    image_path = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=200, blank=False, default='')
    published = models.BooleanField(default=False)
"""

from django.db import models
from datetime import date

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    genre = models.CharField(max_length=30)

    class Meta:
        constraints = [
            # models.UniqueConstraint(Lower('title'), Lower('author'), name='unique_title_author')
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_title_author')

        ]

    def __str__(self):
        return '%s %s %s' % (self.title, self.author, self.genre)


class Member(models.Model):
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    books = models.ManyToManyField(Book, through='Recommendation')

    def __str__(self) -> str:
        return self.name


class Recommendation(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    r_date = models.DateField(default=date.today)
