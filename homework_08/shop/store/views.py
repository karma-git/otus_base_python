from django.shortcuts import render
from django.urls import reverse_lazy
from store.models import Customer, Product
from django.views.generic import ListView, CreateView

# Create your views here.
class CustomerListView(ListView):
    model = Customer

class CustomerCreateView(CreateView):
    model = Customer
    success_url = reverse_lazy('main')
    fields = '__all__'

class ProductListView(ListView):
    model = Product