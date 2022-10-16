from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post
from .forms import PostCreateUpdateForm
from accounts.models import Profile


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

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset)
        post.n_views += 1
        post.save()
        return post


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
        posts = Post.objects.filter(
            ok_to_publish=True, author__user__email=author_email
        )
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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post

    template_name = "blog/post-create.html"
    form_class = PostCreateUpdateForm
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.author = Profile.objects.get(user=self.request.user.id)
        messages.add_message(
            self.request, messages.SUCCESS, "Your post created successfully."
        )
        form.save()
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/post-edit.html"
    form_class = PostCreateUpdateForm

    def get_success_url(self):
        return reverse_lazy("blog:post-detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.save(commit=False)
        if form.instance.author == Profile.objects.get(user=self.request.user.id):
            messages.add_message(
                self.request, messages.SUCCESS, "Post edited successfully."
            )
            form.save()
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post-delete-confirm.html"

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, "Post deleted successfully."
        )
        return reverse_lazy("blog:index")
