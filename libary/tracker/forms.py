from django.forms import ModelForm
from .models import Author

class CreateAuthorForm(ModelForm):
    class Meta:
        model = Author
        fileds=['name']