from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=255)

class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="У книги нет описания :(")
    author = models.ForeignKey(Author,on_delete=models.PROTECT)

class Reader(models.Model):
    name = models.CharField(max_length=255)

class ReaderBookRelationship(models.Model):
    reader = models.ForeignKey(Reader,on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Book,on_delete=models.DO_NOTHING)
    give_date = models.DateTimeField(auto_now_add = True)
    return_date = models.DateTimeField(null = True)