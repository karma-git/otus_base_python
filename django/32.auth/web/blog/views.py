from django.shortcuts import render
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import User

# Create your views here.

class Registration(CreateView):
     model = User
     success_url = reverse_lazy("login")
     form_class = CustomUserCreationForm
