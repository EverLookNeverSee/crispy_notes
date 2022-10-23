from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .serializers import CommentSerializer
from ...models import Comment


class CommentApiView(ListAPIView, CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(
        vary_on_headers(
            "Authorization",
        )
    )
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(email=request.user.email, is_approved=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
