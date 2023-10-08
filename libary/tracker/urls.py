from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'tracker'

urlpatterns = [
    path('author/create/', CreateAuthorView.as_view(), name="create-author"),
    path('author/list/', ListAuthorView.as_view(), name="list-author"),
]