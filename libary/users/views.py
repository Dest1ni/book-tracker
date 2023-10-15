from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as BaseLoginView,LogoutView as BaseLogoutView
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
#    username = forms.ChoiceField(choices=[(user.username,user.username) for user in DefaultUser.objects.all()])
    pass

class RegistrationUserView(CreateView):
    model = DefaultUser
    form_class = CreateUserForm
    template_name = 'users/registration.html' 
    success_url = reverse_lazy("tracker:list-book")

class LoginView(BaseLoginView):
    next_page = reverse_lazy("control:auto-list")
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm
    
class LogoutView(BaseLogoutView):
    #next_page = reverse_lazy("cauth:cauth-login")
    pass

