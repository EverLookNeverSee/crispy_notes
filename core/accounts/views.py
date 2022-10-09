from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text, force_bytes
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .forms import UserRegistrationForm, EmailValidationOnForgotPassword
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


class UserVerificationView(UpdateView):
    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs.get("uidb64")))
            user = User.objects.get(email=uid)
        except User.DoesNotExist:
            user = None
        if user and generate_token.check_token(user, kwargs.get("token")):
            user.is_verified = True
            user.save()
            messages.add_message(
                request, messages.SUCCESS, "Your email verified successfully."
            )
            return redirect("/")
        messages.add_message(request, messages.ERROR, "Something went wrong!")
        return redirect("/")


class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset.html"
    email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset_done")
    form_class = EmailValidationOnForgotPassword


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"
    title = "Password reset completed."
