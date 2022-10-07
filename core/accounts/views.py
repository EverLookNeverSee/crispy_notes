from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import UserRegistrationForm


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
        login(self.request, user)
        return redirect("/")
