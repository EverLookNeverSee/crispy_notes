from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "post", "created_at", "is_approved")
    list_filter = ("is_approved", "created_at")
    search_fields = ("name", "email", "message")
