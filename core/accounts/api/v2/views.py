from rest_framework import generics
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ActivationResendSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from ...models import Profile
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from ..utilities import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings
from accounts.models import User


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"detail": "User created successfully.", "email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token_for_user(user_obj)
            email = EmailMessage(
                template_name="email/activation_email.tpl",
                context={"token": token},
                from_email="from@admin.com",
                to=[email],
            )
            EmailThread(email_obj=email).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_token_for_user(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordAPIView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "Password changed successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(
        vary_on_headers(
            "Authorization",
        )
    )
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class ActivationAPIView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "Token has been expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "Token is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"details": "Your account has already been verified."})
        user_obj.is_verified = True
        user_obj.save()
        return Response({"details": "Your account has been successfully verified."})


class ActivationResendAPIView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request):
        serializer = ActivationResendSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_token_for_user(user_obj)
        email = EmailMessage(
            template_name="email/activation_email.tpl",
            context={"token": token},
            from_email="from@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj=email).start()
        return Response(
            {"details": "Your activation code resend successfully."},
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def get_token_for_user(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
