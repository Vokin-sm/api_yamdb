from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Titles, Categories, Genres, Reviews, Comments, User
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
    """Class for displaying, editing and deleting users."""
    model = User
    serializer_class = UsersSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser
    ]
    queryset = User.objects.all()
    lookup_field = 'username'


class UsersMeAPIView(APIView):
    """Class for displaying and editing your account data."""
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
