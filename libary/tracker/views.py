from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,FormView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from .models import *
from .forms import *
import datetime
# Поменять логику того показывается или нет кнопка юзеру при наличии пермишинов
class CreateAuthorView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = reverse_lazy("users:login-user")
    permission_required = "tracker.add_author"
    model = Author
    fields=['name']
    template_name = "tracker/createauthor.html"
    success_url = reverse_lazy("tracker:list-author")

class ListAuthorView(LoginRequiredMixin,ListView):
    model = Author
    login_url = reverse_lazy("users:login-user")
    template_name = "tracker/listauthor.html"
    context_object_name = "authors"

class CreateBookView(LoginRequiredMixin,PermissionRequiredMixin,FormView): 
    form_class = CreateBookForm
    login_url = reverse_lazy("users:login-user")
    permission_required = "tracker.add_book"
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
            return HttpResponseBadRequest("Кажется вы где-то накосячили")
        
class ListBookView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy("users:login-user")
    template_name = "tracker/allbooks.html"
    model = Book
    context_object_name = "books"
    paginate_by = 10
    def get_queryset(self) -> QuerySet[Any]:
        qs =  Book.objects.filter(amount__gt = 0).order_by('pk').all()
        return qs

class AuthorBookView(LoginRequiredMixin,ListView):
    login_url = reverse_lazy("users:login-user")
    template_name = "tracker/authorbooks.html"
    model = Book
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self, **kwargs: Any) -> dict[str, Any]:
        qs = Book.objects.filter(author = Author.objects.filter(pk = self.kwargs['pk']).first(),amount__gt = 0).order_by('name')
        return qs
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['author'] = Author.objects.filter(pk = self.kwargs['pk']).first()
        return context

class BookDetailView(LoginRequiredMixin,DetailView):
    login_url = reverse_lazy("users:login-user")
    model = Book
    template_name = "tracker/detailbook.html"

class TakeBookView(LoginRequiredMixin,FormView):
    form_class = TakeReturnBookForm
    success_url = reverse_lazy('tracker:list-book')
    template_name = 'tracker/takebook.html'
    def form_valid(self, form: Any) -> HttpResponse:
        if form.is_valid():
            code = form.cleaned_data['code']
            book = Book.objects.filter(amount__gt = 0,pk = code).first()
            if not book:
                return HttpResponseBadRequest("Книги с таким кодом не существует, либо её нет в наличии")
            user = self.request.user
            relation = ReaderBookRelationship(reader = user,book = book)
            book.amount -= 1
            book.save()
            relation.save()
        return super().form_valid(form)

class ReturnBookView(LoginRequiredMixin,FormView):
    form_class = TakeReturnBookForm
    success_url = reverse_lazy('tracker:list-book')
    template_name = 'tracker/returnbook.html'
    def form_valid(self, form: Any) -> HttpResponse:
        if form.is_valid():
            code = form.cleaned_data['code']
            book = Book.objects.filter(pk = code).first()
            user = self.request.user
            meta = ReaderBookRelationship.objects.filter(book_id = code,reader_id = user.pk).first()
            if not meta:
                return HttpResponseBadRequest("Кажется вы ввели неверный код книги, или она уже отдана")
            book.amount += 1
            book.save()
            meta.return_date = datetime.datetime.now()
            meta.save()
        return super().form_valid(form)

class LogsView(LoginRequiredMixin,PermissionRequiredMixin,ListView):

    model = ReaderBookRelationship
    template_name = 'tracker/logs.html'
    permission_required = 'view_logentry'
    context_object_name = 'logs'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        qs = ReaderBookRelationship.objects.select_related('reader','book').order_by('-give_date').all()
        return qs