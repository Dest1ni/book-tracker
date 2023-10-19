from django.forms import ModelForm,Form,IntegerField
from .models import *

class CreateBookForm(ModelForm):
    class Meta:
        model = Book
        fileds = ['name']
        exclude = ['author']

class TakeBookForm(Form):
    code = IntegerField()