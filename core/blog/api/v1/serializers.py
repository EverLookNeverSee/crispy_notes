from rest_framework import serializers
from ...models import Post, Category
from accounts.models import Profile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    summary = serializers.CharField(source="get_summary", read_only=True)
    relative_url = serializers.CharField(source="get_relative_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_absolute_api_url")
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="name", many=True
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "image",
            "content",
            "summary",
            "category",
            "relative_url",
            "absolute_url",
            "ok_to_publish",
            "login_required",
            "n_views",
            "created_at",
            "publish_date",
        ]
        read_only_fields = ["author"]

    def get_absolute_api_url(self, obj):  # It is not a standard and correct method
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        representation = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            representation.pop("summary", None)
            representation.pop("relative_url", None)
            representation.pop("absolute_url", None)
        else:
            representation.pop("content", None)
        # representation["category"] = instance.category.name
        # representation["category"] = CategorySerializer(instance.category.all, context={"request": request}).data
        return representation

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)
