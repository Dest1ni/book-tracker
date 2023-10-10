from django.forms import ModelForm
from .models import *

class CreateBookForm(ModelForm):
    class Meta:
        model = Book
        fileds = ['name']
        exclude = ['author']