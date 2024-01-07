from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from . import forms


# Create your views here.

class SignupView(CreateView):
    form_class = forms.SignupForm
    template_name = 'user_auth/user_auth.html'
    success_url = reverse_lazy('user_auth:login')

class LoginView(LoginView):
    template_name = 'user_auth/user_auth.html'