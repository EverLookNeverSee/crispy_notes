from django import template
from ..models import Comment


register = template.Library()


@register.simple_tag(name="comments_count")
def get_comments_count(pid) -> int:
    """
    Get the number of approved comments of a post
    :param pid: Post id
    :return: int, number of approved comments of the post
    """
    return Comment.objects.filter(post=pid, is_approved=True).count()


@register.inclusion_tag(filename="blog/blog-single-comments.html")
def post_comments(pid):
    """
    Get the number of approved comments of a post
    :param pid: Post id
    :return: int, number of approved comments of the post
    """
    comments = Comment.objects.filter(post=pid, is_approved=True)
    return {"comments": comments}
