from django.urls import path
from .views import *

app_name = "tracker"

urlpatterns = [
    path("author/create/", CreateAuthorView.as_view(), name="create-author"),
    path("author/update/<int:pk>", AuthorUpdate.as_view(), name="update-author"),
    path("author/delete/<int:pk>", AuthorDelete.as_view(), name="delete-author"),
    path("author/list/", ListAuthorView.as_view(), name="list-author"),
    path("author/create-book/<int:id>", CreateBookView.as_view(), name="create-book"),
    path("books/list/", ListBookView.as_view(), name="list-book"),
    path("books/author/<int:pk>", AuthorBookView.as_view(), name="author-book"),
    path("books/detail/<int:pk>", BookDetailView.as_view(), name="detail-book"),
    path("books/take/", TakeBookView.as_view(), name="take-book"),
    path("books/return/", ReturnBookView.as_view(), name="return-book"),
    path("books/logs/", LogsView.as_view(), name="logs-book"),
    path("books/delete/<int:pk>", BookDelete.as_view(), name="book-delete"),
    path("books/update/<int:pk>", BookUpdate.as_view(), name="book-update"),
]
