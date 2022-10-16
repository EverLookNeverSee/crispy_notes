from django import forms
from .models import Post


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image", "ok_to_publish", "login_required", "category"]
