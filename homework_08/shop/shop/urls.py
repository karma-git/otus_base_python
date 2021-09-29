"""shop URL Configuration

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
from django.urls import path
from django.conf.urls import url, include
import store.views as store
from django.views.generic import TemplateView

urlpatterns = [
    path('', store.CustomerListView.as_view(), name='main'),
    path('customer/create/', store.CustomerCreateView.as_view(), name='customer_create'),
    path('customer/detail/<int:pk>/', store.CustomerDetailView.as_view(), name='customer_detail'),
    path('products/', store.ProductListView.as_view(), name='products'),
    path('about/', TemplateView.as_view(template_name='store/about.html'), name='about'),
    path('admin/', admin.site.urls),
    # 3rd party
    url(r'^health_check/', include('health_check.urls')),
]
