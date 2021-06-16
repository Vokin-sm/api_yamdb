from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin

from rest_framework.viewsets import GenericViewSet

from api.models import Titles
from api.models import Categories
from api.models import Genres
from api.models import Reviews
from api.models import Comments
from api.models import User

from api.permissions import IsAdmin
from api.permissions import IsAdminOrReadOnly

from api.serializers import TitlesSerializer
from api.serializers import CategoriesSerializer
from api.serializers import GenresSerializer
from api.serializers import ReviewsSerializer
from api.serializers import CommentsSerializer
from api.serializers import UsersSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    model = Titles
    serializer_class = TitlesSerializer
    queryset = Titles.objects.all()


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
    queryset = Reviews.objects.all()


class CommentsViewSet(viewsets.ModelViewSet):
    model = Comments
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()


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


class UsersMeAPIView(APIView):
    """Class for displaying and editing your account data."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=self.request.user.username)
        serializer = UsersSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = User.objects.get(username=self.request.user.username)
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
