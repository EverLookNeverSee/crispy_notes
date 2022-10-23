from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .paginations import DefaultPagination


class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(ok_to_publish=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        "category__name": ["exact", "in"],
        "author": ["exact"],
        "ok_to_publish": ["exact"],
        "login_required": ["exact"],
    }
    search_fields = ["title", "content"]
    ordering_fields = ["publish_date", "created_at"]
    pagination_class = DefaultPagination

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(
        vary_on_headers(
            "Authorization",
        )
    )
    def retrieve(self, request, *args, **kwargs):
        return super(PostModelViewSet, self).retrieve(request, *args, **kwargs)


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(
        vary_on_headers(
            "Authorization",
        )
    )
    def retrieve(self, request, *args, **kwargs):
        return super(CategoryModelViewSet, self).retrieve(request, *args, **kwargs)
