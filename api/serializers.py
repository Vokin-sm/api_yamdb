from rest_framework import serializers
from rest_framework.validators import ValidationError

from api.models import Titles
from api.models import Categories
from api.models import Genres
from api.models import Reviews
from api.models import Comments
from api.models import User

from django.db.models import Avg


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


class TitlesSerializerGet(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Titles

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score'))
        return rating['score__avg']


class TitlesSerializerPost(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug', many=True)
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = ('__all__')
        model = Titles


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        queryset=Titles.objects.all(),
        slug_field='name',
        required=False
    )

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        title_id = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if Reviews.objects.filter(author=author, title_id=title_id).exists():
            raise ValidationError
        return data

    class Meta:
        fields = ('__all__')
        model = Reviews

class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        fields = (
            'id',
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
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.email = validated_data.get('email', instance.email)
        if instance.role == 'admin' or instance.is_staff:
            instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance
