from django.shortcuts import render
from blog.models import Author, Articles, Tags
from blog.tasks import send_email
from celery import current_app

# Create your views here.
def root(request):
    authors = Author.objects.all()
    # bad query for our index.html
    # authors = Author.objects.only('name').all()
    task_id = None

    # --- celery task
    if request.method == "POST":
        task = send_email.delay("Hello from admin", "I am trying celery")
        task_id = task.id

    return render(request, "blog/index.html", {"authors": authors, "task_id": task_id})

def check_task(request):
    task_id = request.GET.get('task_id', False)
    task = current_app.AsyncResult(task_id)
    task_status = task.status
    return render(request, 'blog/task_status.html', {'task_id': task_id, 'task_status': task_status})


def check_tags(request):
    # tags = Tags.objects.all()
    # prefetch related
    tags = Tags.objects.prefetch_related("articles").all()
    return render(request, "blog/tags.html", {"tags": tags})
