from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import ContactForm


class IndexPageView(TemplateView):
    template_name = "home/index.html"


class AboutPageView(TemplateView):
    template_name = "home/about.html"


class ContactPageView(FormView):
    template_name = "home/contact.html"
    form_class = ContactForm
    success_url = "/"
