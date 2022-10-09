from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes
from .forms import UserRegistrationForm
from .utilities import generate_token, EmailThread
from .models import User


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = "registration/login.html"
    success_url = "/"
    success_message = "You have successfully logged in."
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        auth_logout(request)
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.INFO, "You have successfully logged out."
            )
        next_page = self.get_next_page()
        if next_page:
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)


class CustomSignupView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    success_url = "/"
    success_message = "Your account created successfully and verification email sent."
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save()
        body = render_to_string(
            template_name="registration/verify_account.html",
            context={
                "user": user.email,
                "domain": get_current_site(self.request),
                "uidb64": urlsafe_base64_encode(force_bytes(user)),
                "token": generate_token.make_token(user),
            },
        )
        email_obj = EmailMessage(
            subject="Verify your account",
            body=body,
            from_email="no-reply@crispy-notes.com",
            to=[user.email],
        )
        EmailThread(email_obj).run()
        login(self.request, user)
        return redirect("/")
