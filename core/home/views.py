from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ContactForm


class IndexPageView(TemplateView):
    template_name = "home/index.html"


class AboutPageView(TemplateView):
    template_name = "home/about.html"


class ContactPageView(SuccessMessageMixin, CreateView):
    template_name = "home/contact.html"
    form_class = ContactForm
    success_url = "/"
    success_message = "Your contact form sent successfully."
