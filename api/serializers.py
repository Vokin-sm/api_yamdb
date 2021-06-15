from rest_framework import serializers

# from api.models import Titles
# from api.models import Categories
# from api.models import Genres
# from api.models import Reviews
# from api.models import Comments
from api.models import User


class TitlesSerializer(serializers.ModelSerializer):
    ...


class CategoriesSerializer(serializers.ModelSerializer):
    ...


class GenresSerializer(serializers.ModelSerializer):
    ...


class ReviewsSerializer(serializers.ModelSerializer):
    ...


class CommentsSerializer(serializers.ModelSerializer):
    ...


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
