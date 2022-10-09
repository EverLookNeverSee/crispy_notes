from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.forms import forms
from .models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email, is_verified=True).exists():
            raise forms.ValidationError("There is no user registered with this email address!")
        return email
