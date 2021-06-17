from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Titles
from api.models import Categories
from api.models import Genres
from api.models import Reviews
from api.models import Comments
from api.models import User


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Titles


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug'
        )
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name',
            'slug'
        )
        model = Genres


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'text',
            'author',
            'score',
            'pub_date'
        )
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'text',
            'author',
            'pub_date'
        )
        model = Comments


class UsersSerializer(serializers.ModelSerializer):
    """Serialization of users."""

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
        model = User


class UsersMeSerializer(serializers.ModelSerializer):
    """Serialization of users.me"""

    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
        model = User

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.email = validated_data.get('email', instance.email)
        if instance.role == 'admin' or instance.is_staff:
            instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     username_field = get_user_model().email
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['confirmation_code'] = serializers.CharField(required=True)
#         self.fields.pop('password')
