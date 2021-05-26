from rest_framework import serializers
from django.contrib.auth.models import User
from social_app.models import Post, Like
from social_app.utils import abstract_api_email_validate, abstract_api_get_ipgeolocation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "date_joined",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        import asyncio

        password = validated_data.pop("password")
        user = User(**validated_data)

        is_email_valid = abstract_api_email_validate(validated_data.get("email"))

        if is_email_valid == True:
            user.set_password(password)
            user.save()
            abstract_api_get_ipgeolocation(user.username)
            return user
        raise serializers.ValidationError(
            {"error": "Email provided is not valid, Try valid one"}
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "user", "title", "content", "like_count")
        extra_kwargs = {"like_count": {"read_only": True}, "user": {"read_only": True}}


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "user", "post")
        extra_kwargs = {"user": {"read_only": True}}
