from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView
from .models import *

class CreateAuthorView(CreateView):
    model = Author
    fields=['name']
    template_name = "tracker/createauthor.html"
    success_url = reverse_lazy("tracker:list-author")

class ListAuthorView(ListView):
    model = Author
    template_name = "tracker/listauthor.html"
    context_object_name = "authors"