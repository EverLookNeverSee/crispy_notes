from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ContactForm
from blog.models import Post, Category


class IndexPageView(TemplateView):
    template_name = "home/index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        normal_posts = Post.objects.filter(ok_to_publish=True, login_required=False)[:7]
        recommended_posts = Post.objects.filter(
            ok_to_publish=True, login_required=False
        )[10:13]
        top_viewed_posts = Post.objects.filter(
            ok_to_publish=True, login_required=False
        ).order_by("-n_views")[:3]
        categories = Category.objects.all()
        context["normal_posts"] = normal_posts
        context["recommended_posts"] = recommended_posts
        context["top_viewed_posts"] = top_viewed_posts
        context["categories"] = categories
        return self.render_to_response(context)


class AboutPageView(TemplateView):
    template_name = "home/about.html"


class ContactPageView(SuccessMessageMixin, CreateView):
    template_name = "home/contact.html"
    form_class = ContactForm
    success_url = "/"
    success_message = "Your contact form sent successfully."
