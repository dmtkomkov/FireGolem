from django.shortcuts import redirect
from django.http import HttpResponse
from blog.models import Post


def index(request):
    return HttpResponse("<h2>Hello World!</h2>")


def post(request):
    data = request.POST
    title = data.get('title')
    post = data.get('post')
    print(title, post)
    db_post = Post(title=title, body=post)
    db_post.save()
    return redirect('/blog/', permanent=True)
