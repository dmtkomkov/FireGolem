from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache

from api.models import Post
from helpers.pagination import get_page


class BlogView(LoginRequiredMixin, View):
    def get(self, request):
        all_posts = Post.objects.all().order_by("-created")
        blog_filter = request.GET.get('filter')
        if blog_filter == 'post':
            all_posts = all_posts.filter(worklog__isnull=True)
        elif blog_filter == 'worklog':
            all_posts = all_posts.filter(worklog__isnull=False)

        post_count = cache.get('post_count', Post.objects.filter(worklog__isnull=True).count())
        cache.add('post_count', post_count)
        worklog_count = cache.get('worklog_count', Post.objects.filter(worklog__isnull=False).count())
        cache.add('worklog_count', worklog_count)
        blog_len = post_count + worklog_count

        active_page = request.GET.get('page')

        posts, page_conf = get_page(all_posts, active_page)
        page = {
            'posts': posts,
            'blog_len': blog_len,
            'post_count': post_count,
            'worklog_count': worklog_count,
        }
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
