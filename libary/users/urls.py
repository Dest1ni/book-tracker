from django.contrib import admin
from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login-user"),
    path("registration/", RegistrationUserView.as_view(), name="registration-user"),
    path("logout/", LogoutView.as_view(), name="logout-user"),
]
