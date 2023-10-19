from typing import Any
from django import forms
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as BaseLoginView,LogoutView as BaseLogoutView
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
    

class RegistrationUserView(CreateView):
    model = DefaultUser
    form_class = CreateUserForm
    template_name = 'users/registration.html' 
    success_url = reverse_lazy("tracker:list-book")
    def form_valid(self, form):
        user:DefaultUser = form.save(commit=False)
        last_name,first_name,patronymic =  user.name.split(' ')
        user.last_name,user.first_name,user.patronymic = last_name,first_name,patronymic
        user.username = last_name + '_' + str(DefaultUser.objects.count() + 1)
        user.save()
        return super().form_valid(form)
    
class LoginView(BaseLoginView):
    next_page = reverse_lazy("tracker:list-book")
    template_name = 'users/login.html'
    form_class = CustomAuthenticationForm
    
class LogoutView(BaseLogoutView):
    next_page = reverse_lazy("users:login-user")

