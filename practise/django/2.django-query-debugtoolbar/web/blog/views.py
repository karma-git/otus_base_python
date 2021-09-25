from django.shortcuts import render
from blog.models import Author

# Create your views here.
def root(request):
    authors = Author.objects.all()
    return render(request, 'blog/index.html', {'authors': authors})
