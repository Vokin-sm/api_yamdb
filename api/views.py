import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.filters import TitlesFilter
from api.models import Categories, Comments, Genres, Reviews, Titles, User
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsOwnerOrAdminOrModeratorOrReadOnly)
from api.serializers import (CategoriesSerializer, CommentsSerializer,
                             EmailSerializer, GenresSerializer,
                             LoginSerializer, ReviewsSerializer,
                             TitlesSerializerGet, TitlesSerializerPost,
                             UsersMeSerializer, UsersSerializer)
from api_yamdb import settings


class TitlesViewSet(viewsets.ModelViewSet):
    """Class for displaying, creating, editing and deleting titles."""

    queryset = Titles.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitlesSerializerGet
        return TitlesSerializerPost


class LCDViewSet(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin,
                 GenericViewSet):
    """This class can 'List', 'Create', 'Destroy' objects"""

    pass


class CategoriesViewSet(LCDViewSet):
    """Class for displaying, creating and deleting categories."""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenresViewSet(LCDViewSet):
    """Class for displaying, creating and deleting genres."""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class ReviewsViewSet(viewsets.ModelViewSet):
    """Class for displaying, creating, editing and deleting reviews."""

    model = Reviews
    serializer_class = ReviewsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrAdminOrModeratorOrReadOnly
    ]

    def get_queryset(self):
        reviews = Reviews.objects.all()
        title_id = self.kwargs['title_id']
        queryset = reviews.filter(title_id=title_id)
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Class for displaying, creating, editing and deleting comments."""

    model = Comments
    serializer_class = CommentsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrAdminOrModeratorOrReadOnly
    ]

    def get_queryset(self):
        comments = Comments.objects.all()
        review_id = self.kwargs['review_id']
        queryset = comments.filter(review_id=review_id)
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Reviews, id=review_id)
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(viewsets.ModelViewSet):
    """Class for displaying, editing and deleting users."""
    model = User
    serializer_class = UsersSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdmin,
    ]
    queryset = User.objects.all()
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        user = User.objects.get(username=self.request.user.username)
        if request.method == 'GET':
            serializer = UsersMeSerializer(user)
            return Response(serializer.data)
        serializer = UsersMeSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code_create_user(request):
    """Creates a user and sends him a confirmation code by email."""
    confirmation_code = random.randint(111111, 999999)
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data['email'].split('@')[0]
    User.objects.create_user(
        request.data['email'],
        username=username,
        password='',
        confirmation_code=confirmation_code
    )
    send_mail(
        'Подтверждение почты',
        f'{confirmation_code}',
        settings.EMAIL_HOST_USER,
        [request.data['email']]
    )
    return Response(request.data, status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    """Issues a jwt token to the user."""
    serializer_class = LoginSerializer
