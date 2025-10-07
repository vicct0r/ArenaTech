from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.conf import settings

from .forms import CustomUserCreationForm, CustomUserChangeForm


class UserSignupView(generic.CreateView):
    template_name = 'usuarios/signup.html'
    model = settings.AUTH_USER_MODEL
    form_class = CustomUserCreationForm
