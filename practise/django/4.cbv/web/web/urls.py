"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import blog.views as blog
from web.settings import DEBUG
from django.views.generic import TemplateView

urlpatterns = [
    # path('', blog.root),  # Deeprecated FBV
    path('', blog.AuthorListView.as_view()),
    # path('authors', blog.AuthorDetailView.as_view(template_name='blog/authors.html')),
    path('tags/', blog.check_tags),
    path('about/', TemplateView.as_view(template_name='blog/about.html')),
    path('admin/', admin.site.urls),
]

if DEBUG:
    import debug_toolbar

    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)),)
