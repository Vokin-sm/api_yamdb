import random

from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework import filters
from rest_framework.decorators import api_view, action
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin

from django.shortcuts import get_object_or_404

from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Titles
from api.models import Categories
from api.models import Genres
from api.models import Reviews
from api.models import Comments
from api.models import User

from api.permissions import IsAdmin
from api.permissions import IsAdminOrReadOnly
from api.permissions import IsOwnerOrAdminOrModeratorOrReadOnly


from api.serializers import LoginSerializer
from api.serializers import TitlesSerializerGet
from api.serializers import TitlesSerializerPost
from api.serializers import CategoriesSerializer
from api.serializers import GenresSerializer
from api.serializers import ReviewsSerializer
from api.serializers import CommentsSerializer
from api.serializers import UsersSerializer
from api.serializers import UsersMeSerializer
from api_yamdb import settings

from api.filters import TitlesFilter


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitlesSerializerGet
        return TitlesSerializerPost


class LCDViewSet(ListModelMixin,
                 CreateModelMixin,
                 DestroyModelMixin,
                 GenericViewSet):
    pass


class CategoriesViewSet(LCDViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenresViewSet(LCDViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class ReviewsViewSet(viewsets.ModelViewSet):
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
        title = get_object_or_404(Titles, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    model = Comments
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()
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
        review_id = self.kwargs['review_id']
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

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated])
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
