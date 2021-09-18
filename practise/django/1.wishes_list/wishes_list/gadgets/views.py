from django.shortcuts import render

from gadgets.models import Gadget

# Create your views here.
# FBV
def read_root(request):
    gadgets = Gadget.objects.all()
    return render(request, "gadgets/index.html", context={"gadgets": gadgets})
