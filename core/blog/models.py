from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True, upload_to="blog/", default="blog/default.jpg")
    content = models.TextField()
    category = models.ManyToManyField(Category)
    n_views = models.PositiveIntegerField(default=0)
    ok_to_publish = models.BooleanField(default=False)
    login_required = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("blog:single", kwargs={"pid": self.id})
