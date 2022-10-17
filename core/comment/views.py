from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Comment
from .forms import CommentForm
from blog.models import Post
from accounts.models import Profile, User


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = "blog/blog-single-add-comment.html"
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Your comment posted successfully and will be published after approvement.",
        )
        return reverse_lazy("blog:post-detail", kwargs={"pk": self.kwargs.get("pk")})

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.post = Post.objects.get(pk=self.kwargs.get("pk"))
        user = get_object_or_404(User, email=self.request.POST.get("name"))
        profile = Profile.objects.get(user_id=user)
        form.instance.name = f"{profile.first_name} {profile.last_name}"
        form.instance.email = self.request.POST.get("email")
        form.save()
        return super(CommentCreateView, self).form_valid(form)
