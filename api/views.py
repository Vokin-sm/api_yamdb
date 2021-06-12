from rest_framework import viewsets

from api.models import Titles, Categories, Genres, Reviews, Comments
from api.serializers import (TitlesSerializer, CategoriesSerializer,
                             GenresSerializer, ReviewsSerializer,
                             CommentsSerializer, UsersSerializer)


class TitlesViewSet(viewsets.ModelViewSet):
    ...


class CategoriesViewSet(viewsets.ModelViewSet):
    ...


class GenresViewSet(viewsets.ModelViewSet):
    ...


class ReviewsViewSet(viewsets.ModelViewSet):
    ...


class CommentsViewSet(viewsets.ModelViewSet):
    ...


class UsersViewSet(viewsets.ModelViewSet):
    ...
