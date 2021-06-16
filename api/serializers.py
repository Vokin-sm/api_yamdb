from rest_framework import serializers

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
