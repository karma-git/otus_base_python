from django.shortcuts import render
from django.urls import reverse_lazy
from .models import User, Product
from django.views.generic import ListView, CreateView, DetailView, UpdateView

# Create your views here.
# class ProductListView(ListView):
#     model = Product

# class CustomerCreateView(CreateView):
#     model = Customer
#     success_url = reverse_lazy("main")
#     form_class = CustomerForm


# class CustomerUpdateView(UpdateView):
#     model = Customer
#     form_class = CustomerForm

#     def get_success_url(self):
#         return reverse_lazy("customer_detail", kwargs={"pk": self.object.id})


# class CustomerDetailView(DetailView):
#     model = Customer


class ProductListView(ListView):
    model = Product
