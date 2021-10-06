from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from .models import User, Article, Tag

# Create your views here.

class Registration(CreateView):
     model = User
     success_url = reverse_lazy("login")
     form_class = CustomUserCreationForm

class ArticlesListView(LoginRequiredMixin, ListView):
    model = Article
    queryset = Article.objects.only('title', 'author__username').select_related('author')
    login_url = 'login'
    redirect_field_name = 'articles'
