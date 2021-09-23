from django.shortcuts import render
from store.models import Customer

# Create your views here.
def index_view(request):
    customers = Customer.objects.all()
    return render(request, "store/index.html", context={"customers": customers})
