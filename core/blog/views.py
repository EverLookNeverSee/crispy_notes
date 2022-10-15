from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from .models import Post, Category


class BlogIndexView(ListView):
    template_name = "blog/blog-index.html"
    model = Post
    queryset = Post.objects.filter(ok_to_publish=True, login_required=False)
    context_object_name = "posts"
    paginate_by = 9