from django import template
from ..models import Post, Category

register = template.Library()


@register.inclusion_tag(filename="home/footer_recommended_posts.html")
def footer_recommended_posts():
    recommended_posts = Post.objects.filter(ok_to_publish=True, login_required=False)[10:13]
    return {"frp": recommended_posts}


@register.inclusion_tag(filename="home/footer_all_categories.html")
def footer_all_categories():
    all_cats = Category.objects.all()
    return {"categories": all_cats}


@register.inclusion_tag(filename="blog/blog-single-all-categories.html")
def blog_single_all_categories():
    all_cats = Category.objects.all()
    return {"categories": all_cats}
