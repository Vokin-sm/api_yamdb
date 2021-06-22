from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import (PasswordField,
                                                  TokenObtainPairSerializer)

from api.models import Categories, Comments, Genres, Reviews, Titles, User


class CategoriesSerializer(serializers.ModelSerializer):
    """Is used to serialize categories."""

    class Meta:
        model = Categories
        exclude = ['id']


class GenresSerializer(serializers.ModelSerializer):
    """Is used to serialize genres."""

    class Meta:
        model = Genres
        exclude = ['id']


class TitlesSerializerGet(serializers.ModelSerializer):
    """Is used to serialize GET requests for titles"""

    genre = GenresSerializer(
        many=True,
        read_only=True
    )
    category = CategoriesSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        ]
        model = Titles

    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score'))
        return rating['score__avg']


class TitlesSerializerPost(serializers.ModelSerializer):
    """Is used to serialize POST requests for titles."""

    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )

    class Meta:
        fields = '__all__'
        model = Titles


class ReviewsSerializer(serializers.ModelSerializer):
    """Is used to serialize reviews."""

    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
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
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        )
        model = Reviews


class CommentsSerializer(serializers.ModelSerializer):
    """Is used to serialize comments."""
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
    """Is used to serialize users."""

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
    """Is used to serialize model of current user."""
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
            'first_name',
            instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name',
            instance.last_name
        )
        instance.username = validated_data.get(
            'username',
            instance.username
        )
        instance.bio = validated_data.get(
            'bio',
            instance.bio
        )
        instance.email = validated_data.get(
            'email',
            instance.email
        )

        if instance.role == 'admin' or instance.is_staff:
            instance.role = validated_data.get(
                'role',
                instance.role
            )
        instance.save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):
    """Is used to serialize confirmation code for JWT Token."""
    email = serializers.EmailField()
    confirmation_code = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(default=None)
        self.fields['password'] = PasswordField(default=None)

    def validate(self, data):
        user = User.objects.get(email=data['email'])
        if data['confirmation_code'] != user.confirmation_code:
            raise ValidationError('Вы ввели неправильный код')
        user.is_active = True
        user.save()
        data = {}
        refresh = self.get_token(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class EmailSerializer(serializers.ModelSerializer):
    """Is used to serialize users email."""

    class Meta:
        fields = ('email',)
        model = User
