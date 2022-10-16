from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Category


# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    list_display = (
        "author",
        "title",
        "ok_to_publish",
        "login_required",
        "created_at",
        "publish_date",
    )
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    summernote_fields = ("content",)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
