from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from api.models import Titles
from api.models import Categories
from api.models import Genres
from api.models import Reviews
from api.models import Comments
from api.models import User
from api.permissions import IsAdmin
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


class CategoriesViewSet(viewsets.ModelViewSet):
    model = Categories
    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()


class GenresViewSet(viewsets.ModelViewSet):
    model = Genres
    serializer_class = GenresSerializer
    queryset = Genres.objects.all()


class ReviewsViewSet(viewsets.ModelViewSet):
    model = Reviews
    serializer_class = ReviewsSerializer
    queryset = Reviews.objects.all()

    def get_queryset(self):
        reviews = Reviews.objects.all()
        title_id = self.kwargs['title_id']
        queryset = reviews.filter(title_id=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        serializer.save(author=self.request.user, post_id=title_id)


class CommentsViewSet(viewsets.ModelViewSet):
    model = Comments
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()

    def get_queryset(self):
        comments = Comments.objects.all()
        review_id = self.kwargs['review_id']
        queryset = comments.filter(review_id=review_id)
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        serializer.save(author=self.request.user, post_id=review_id)


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
