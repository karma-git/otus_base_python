from django.shortcuts import render
from store.models import Customer
from django.views.generic import ListView

# Create your views here.
class CustomerListView(ListView):
    model = Customer
