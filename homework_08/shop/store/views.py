from django.shortcuts import render
from django.urls import reverse_lazy
from store.forms import CustomerForm
from store.models import Customer, Product
from django.views.generic import ListView, CreateView, DetailView, UpdateView

# Create your views here.
class CustomerListView(ListView):
    model = Customer

class CustomerCreateView(CreateView):
    model = Customer
    success_url = reverse_lazy('main')
    form_class = CustomerForm

class CustomerUpdateView(UpdateView):
    model = Customer
    success_url = reverse_lazy('main') # TODO return customer_detail current user
    form_class = CustomerForm

class CustomerDetailView(DetailView):
    model = Customer

class ProductListView(ListView):
    model = Product
