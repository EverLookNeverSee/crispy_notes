from rest_framework import serializers
from comment.models import Comment
from accounts.models import Profile


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "post", "name", "email", "message", "is_approved", "created_at"]
        read_only_fields = ["name", "email", "is_approved"]

    def create(self, validated_data):
        profile = Profile.objects.get(user__id=self.context.get("request").user.pk)
        validated_data["name"] = f"{profile.first_name} {profile.last_name}"
        validated_data["email"] = self.context.get("request").user.email
        return super(CommentSerializer, self).create(validated_data)
