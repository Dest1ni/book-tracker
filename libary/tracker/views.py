from typing import Any
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,FormView,TemplateView,DetailView
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from .models import *
from .forms import *

class CreateAuthorView(CreateView):
    model = Author
    fields=['name']
    template_name = "tracker/createauthor.html"
    success_url = reverse_lazy("tracker:list-author")

class ListAuthorView(ListView):
    model = Author
    template_name = "tracker/listauthor.html"
    context_object_name = "authors"

class CreateBookView(FormView):
    form_class = CreateBookForm
    template_name = "tracker/createbook.html"
    success_url = reverse_lazy("tracker:list-author")

    def form_valid(self, form): 
        # Тут не нужна перечада формы, она передается автоматом
        if form.is_valid():
            name = form.cleaned_data['name']
            book = Book(
                name=name,
                author=Author.objects.filter(pk=self.kwargs['id']).first()
            )
            book.save()
            return super().form_valid(form)
        else:
            raise HttpResponseBadRequest()
        
class ListBookView(TemplateView):
    template_name = "tracker/allbooks.html"

class AuthorBookView(TemplateView):
    template_name = "tracker/authorbooks.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        author_id = self.kwargs['id']
        print(author_id)
        context['author'] = Author.objects.filter(pk = author_id).first()
        print(context['author'])
        print(context['author'].pk)
        return context

class BookDetail(DetailView):
    model = Book
    template_name = "tracker/detailbook.html"