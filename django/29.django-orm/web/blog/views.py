from django.shortcuts import render
from blog.models import  (
    Author, 
    Articles,
    Tags
)

# Create your views here.
def root(request):
    authors = Author.objects.all()
    # bad query for our index.html
    # authors = Author.objects.only('name').all()
    return render(request, 'blog/index.html', {'authors': authors})

def check_tags(request):
    # tags = Tags.objects.all()
    # prefetch related
    tags = Tags.objects.prefetch_related('articles').all()
    return render(request, 'blog/tags.html', {'tags': tags})
