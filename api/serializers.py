from rest_framework import serializers

from api.models import Titles, Categories, Genres, Reviews, Comments


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
    ...