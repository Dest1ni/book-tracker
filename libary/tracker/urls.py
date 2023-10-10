from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'tracker'

urlpatterns = [
    path('author/create/', CreateAuthorView.as_view(), name="create-author"),
    path('author/list/', ListAuthorView.as_view(), name="list-author"),
    path('author/create-book/<int:id>', CreateBookView.as_view(), name="create-book"),    
    path('books/list/', ListBookView.as_view(), name="list-book"),
    path('books/author/<int:id>', AuthorBookView.as_view(), name="author-book"),    
]