from django.db import models
from users.models import DefaultUser


class Author(models.Model):
    name = models.CharField(max_length=255)

    def get_absolute_url(self):
        from django.urls import reverse_lazy

        return reverse_lazy("tracker:author-book", kwargs={"pk": self.pk})


class Book(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="У книги нет описания :(")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


class ReaderBookRelationship(models.Model):
    reader = models.ForeignKey(DefaultUser, on_delete=models.CASCADE)  # Доделать логику
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    give_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True)
