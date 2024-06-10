from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    FormView,
    DetailView,
    View,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from .models import *
from .forms import *
from django.utils import timezone
from django.core.paginator import Paginator


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
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        qs = Author.objects.all().order_by("name")
        return qs

    def post(self, request, *args, **kwargs):
        authors = self.get_queryset()
        name = request.POST.get("author")
        if name:
            authors = authors.filter(name__icontains=name)
        paginator = Paginator(authors, self.paginate_by)
        page_number = request.POST.get("page") or 1
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "tracker/listauthor.html",
            {"authors": authors.all(), "page_obj": page_obj},
        )


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
        qs = (
            super()
            .get_queryset()
            .select_related("author")
            .filter(amount__gt=0)
            .order_by("name")
            .all()
        )
        return qs

    def post(self, request, *args, **kwargs):
        book_name = request.POST.get("name")
        author_name = request.POST.get("author")
        id = request.POST.get("id")
        books = self.get_queryset()
        if book_name:
            books = books.filter(name__icontains=book_name)
        if author_name:
            books = books.filter(author__name__icontains=author_name)
        if id:
            books = books.filter(pk__icontains=id)
        paginator = Paginator(books, self.paginate_by)
        page_number = request.POST.get("page") or 1
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "tracker/allbooks.html",
            {"books": books.order_by("name").all(), "page_obj": page_obj},
        )


class AuthorBookView(LoginRequiredMixin, ListView):
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
        context = super().get_context_data()
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
                book_id=code, reader_id=user.pk, return_date=None
            ).first()
            if not meta:
                return HttpResponseBadRequest(
                    "Кажется вы ввели неверный код книги, или она уже отдана"
                )
            book.amount += 1
            book.save()
            meta.return_date = timezone.now()
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
        paginator = Paginator(logs, self.paginate_by)
        page_number = request.POST.get("page") or 1
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "tracker/logs.html",
            {"logs": logs.order_by("-give_date").all(), "page_obj": page_obj},
        )


class Redirect(View):  # Oh god forgive me

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy("tracker:list-author"))


class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "change_author"
    permission_denied_message = "У вас нет прав доступа"
    model = Author
    fields = ["name"]
    template_name = "tracker/update_author.html"


class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "delete_author"
    permission_denied_message = "У вас нет прав доступа"
    model = Author
    template_name = "tracker/delete_author.html"
    success_url = reverse_lazy("tracker:list-author")

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        books = Book.objects.filter(author=pk).all()
        given = ReaderBookRelationship.objects.filter(
            book__in=books, return_date=None
        ).all()
        if given:
            error_message = "Нельзя удалить автора книги которого не сданы !"
            return render(
                self.request,
                self.template_name,
                {"form": form, "error_message": error_message},
            )
        return super().form_valid(form)
