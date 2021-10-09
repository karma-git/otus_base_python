from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
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

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_article'
    model = Article
    success_url = 'articles'
    fields = "__all__"

class ArticleDetail(PermissionRequiredMixin, DetailView):
     model = Article
     permission_required = 'blog.view_article'
     queryset = Article.objects.only('title', 'text', 'author__username').select_related('author')

class ArticleUpdate(UpdateView):
     pass

class ArticleDelete(DeleteView):
     pass
