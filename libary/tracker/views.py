from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from .models import *
from .forms import *
import datetime
from django.db.models.functions import Lower


class CreateAuthorView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = reverse_lazy("users:login-user")
    permission_required = "tracker.add_author"
    model = Author
    fields = ["name"]
    template_name = "tracker/createauthor.html"
    success_url = reverse_lazy("tracker:list-author")


class ListAuthorView(LoginRequiredMixin, ListView):
    model = Author
    login_url = reverse_lazy("users:login-user")
    template_name = "tracker/listauthor.html"
    context_object_name = "authors"


class CreateBookView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = CreateBookForm
    login_url = reverse_lazy("users:login-user")
    permission_required = "tracker.add_book"
    template_name = "tracker/createbook.html"
    success_url = reverse_lazy("tracker:list-author")

    def form_valid(self, form):
        # Тут не нужна перечада формы, она передается автоматом
        if form.is_valid():
            name = form.cleaned_data["name"]
            amount = form.cleaned_data["amount"]
            book = Book(
                name=name,
                author=Author.objects.filter(pk=self.kwargs["id"]).first(),
                amount=amount,
            )
            book.save()
            return super().form_valid(form)
        else:
            return HttpResponseBadRequest("Кажется вы где-то накосячили")


class ListBookView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("users:login-user")
    template_name = "tracker/allbooks.html"
    model = Book
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset().select_related("author").filter(amount__gt=0).all()
        return qs


class AuthorBookView(ListView, LoginRequiredMixin):
    login_url = reverse_lazy("users:login-user")
    template_name = "tracker/authorbooks.html"
    model = Book
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self, **kwargs: Any) -> dict[str, Any]:
        qs = (
            super()
            .get_queryset()
            .filter(
                author=Author.objects.filter(pk=self.kwargs["pk"]).first(), amount__gt=0
            )
            .order_by("name")
            .all()
        )
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["author"] = Author.objects.filter(pk=self.kwargs["pk"]).first()
        return context


class BookDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy("users:login-user")
    model = Book
    template_name = "tracker/detailbook.html"


class TakeBookView(LoginRequiredMixin, FormView):
    form_class = TakeReturnBookForm
    success_url = reverse_lazy("tracker:list-book")
    template_name = "tracker/takebook.html"

    def form_valid(self, form: Any) -> HttpResponse:
        if form.is_valid():
            code = form.cleaned_data["code"]
            book = Book.objects.filter(amount__gt=0, pk=code).first()
            if not book:
                return HttpResponseBadRequest(
                    "Книги с таким кодом не существует, либо её нет в наличии"
                )
            user = self.request.user
            relation = ReaderBookRelationship(reader=user, book=book)
            book.amount -= 1
            book.save()
            relation.save()
        return super().form_valid(form)


class ReturnBookView(LoginRequiredMixin, FormView):
    form_class = TakeReturnBookForm
    success_url = reverse_lazy("tracker:list-book")
    template_name = "tracker/returnbook.html"

    def form_valid(self, form: Any) -> HttpResponse:
        if form.is_valid():
            code = form.cleaned_data["code"]
            book = Book.objects.filter(pk=code).first()
            user = self.request.user
            meta = ReaderBookRelationship.objects.filter(
                book_id=code, reader_id=user.pk
            ).first()
            if not meta:
                return HttpResponseBadRequest(
                    "Кажется вы ввели неверный код книги, или она уже отдана"
                )
            book.amount += 1
            book.save()
            meta.return_date = datetime.datetime.now()
            meta.save()
        return super().form_valid(form)


class LogsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):

    model = ReaderBookRelationship
    template_name = "tracker/logs.html"
    permission_required = "view_logentry"
    context_object_name = "logs"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        qs = (
            super()
            .get_queryset()
            .select_related("reader", "book")
            .order_by("-give_date")
            .all()
        )  # Replaced Model.objects everywhere mb this work better
        return qs

    def post(self, request, *args, **kwargs):
        book_name = request.POST.get("name")
        give_year = request.POST.get("give_year")
        give_month = request.POST.get("give_month")
        give_day = request.POST.get("give_day")
        return_year = request.POST.get("return_year")
        return_month = request.POST.get("return_month")
        return_day = request.POST.get("return_day")
        username = request.POST.get("username")
        id = request.POST.get("id")
        logs = self.get_queryset()
        if book_name:
            logs = logs.filter(
                book__name__icontains=book_name
            )  # SQLite doesnt work with icontain because ASSCII
        if give_year:
            logs = logs.filter(give_date__year__contains=give_year)
        if give_day:
            logs = logs.filter(give_date__day__contains=give_day)
        if give_month:
            logs = logs.filter(give_date__month__contains=give_month)
        if return_year:
            logs = logs.filter(return_date__year__contains=return_year)
        if return_day:
            logs = logs.filter(return_date__day__contains=return_day)
        if return_month:
            logs = logs.filter(return_date__month__contains=return_month)
        if username:
            logs = logs.filter(reader__name__icontains=username)
        if id:
            logs = logs.filter(book__pk__icontains=id)
        return render(
            request, "tracker/logs.html", {"logs": logs.order_by("-give_date").all()}
        )


class Redirect(View):  # Oh god forgive me

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy("tracker:list-author"))
