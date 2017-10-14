from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from api.models import Post
from helpers.pagination import get_page

PPP = 10  # POSTS_PER_PAGE
PML = 11  # PAGINATOR_MAX_LENGTH
PHL = (PML - 1) // 2 # PAGINATOR_HALF_LENGTH


class BlogView(LoginRequiredMixin, View):
    def get(self, request):
        all_posts = Post.objects.all().filter(deleted=False).order_by("created")
        active_page = request.GET.get('page')

        posts, page_conf = get_page(all_posts, active_page)
        page = {'posts': posts}
        page.update(page_conf)

        return render(request, 'blog/home.html', page)

    def post(self, request):
        title = request.POST.get('title')
        post = request.POST.get('body')
        db_post = Post(title=title, body=post)
        db_post.user = request.user
        db_post.save()
        return self.get(request)

    def put(self, request):
        post_id = request.PUT['post_id']
        oPost = Post.objects.get(id=post_id)
        oPost.title = request.PUT['title']
        oPost.body = request.PUT['body']
        oPost.save()
        return self.get(request)

    def delete(self, request):
        post_id = request.DELETE['post_id']
        oPost = Post.objects.get(id=post_id)
        oPost.deleted = True
        oPost.save()
        return self.get(request)
