from django.shortcuts import render
from django.urls import reverse_lazy
from .models import User, Product
from .forms import CustomUserCreationForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

class Registration(CreateView):
     model = User
     success_url = reverse_lazy("login")
     form_class = CustomUserCreationForm

class ProductDetailView(LoginRequiredMixin, DetailView):
     model = Product

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'store.add_product'
    model = Product
    success_url = reverse_lazy('products')
    fields = ('goods', 'description', 'price',)

class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'store.change_product'
    fields = ('goods', 'description', 'price',)

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.object.id})

class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'store.delete_product'
    success_url = reverse_lazy('products')
    fields = "__all__"
