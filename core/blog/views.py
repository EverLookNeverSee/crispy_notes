from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from .models import Post, Category


class BlogIndexView(LoginRequiredMixin, ListView):
    template_name = "blog/blog-index.html"
    model = Post
    queryset = Post.objects.filter(ok_to_publish=True, login_required=True)
    context_object_name = "posts"
    paginate_by = 9


class PostDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    template_name = "blog/blog-single.html"
    permission_required = "blog.view_post"
    model = Post


class CategoryFilterPostListView(LoginRequiredMixin, ListView):
    template_name = "blog/blog-index.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        category_name = self.kwargs.get("cat_name")
        posts = Post.objects.filter(ok_to_publish=True, category__name=category_name)
        return posts


class AuthorFilterPostListView(LoginRequiredMixin, ListView):
    template_name = "blog/blog-index.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        author_email = self.kwargs.get("author_email")
        posts = Post.objects.filter(ok_to_publish=True, author__user__email=author_email)
        return posts


class SearchPostListView(LoginRequiredMixin, ListView):
    template_name = "blog/blog-index.html"
    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        s = self.request.GET.get("s")
        posts = Post.objects.filter(ok_to_publish=True)
        posts = posts.filter(Q(title__icontains=s) | Q(content__icontains=s))
        return posts
