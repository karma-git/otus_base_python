from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
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

class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_article'
    model = Article
    success_url = reverse_lazy('articles')
    fields = "__all__"

class ArticleDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
     model = Article
     permission_required = 'blog.view_article'
     queryset = Article.objects.only('title', 'text', 'author__username').select_related('author')


class ArticleTestMixin(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin):
     model = Article
     lookup = 'pk'

     def test_func(self):
          article_author_username = (
               self.model.objects.filter(id=self.kwargs[self.lookup])
               .only('author__username').select_related('author').first()
               .author.username
          )
          current_username = self.request.user.username
          is_author = True if article_author_username == current_username else False
          is_moderator = self.request.user.groups.filter(Q(name='Moderator') | Q(name='Judge')).exists()
          print(is_author, is_moderator)
          return is_author or is_moderator


class ArticleUpdate(ArticleTestMixin, UpdateView):
     model = Article
     permission_required = 'blog.change_article'
     fields = ('title', 'text',)

     def get_success_url(self):
          return reverse_lazy("article_detail", kwargs={"pk": self.object.id})


class ArticleDelete(ArticleTestMixin, DeleteView):
     model = Article
     permission_required = 'blog.delete_article'
     success_url = reverse_lazy('articles')
     fields = "__all__"
