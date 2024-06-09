from django.db import models
from users.models import DefaultUser


class Author(models.Model):
    name = models.CharField(max_length=255)


class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="У книги нет описания :(")
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    amount = models.IntegerField(default=0)


class ReaderBookRelationship(models.Model):
    reader = models.ForeignKey(
        DefaultUser, on_delete=models.DO_NOTHING
    )  # Доделать логику
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    give_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True)
