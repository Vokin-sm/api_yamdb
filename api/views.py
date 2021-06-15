from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

# from api.models import Titles
# from api.models import Categories
# from api.models import Genres
# from api.models import Reviews
# from api.models import Comments
from api.models import User
# from api.permissions import IsAdmin
# from api.serializers import TitlesSerializer
# from api.serializers import CategoriesSerializer
# from api.serializers import GenresSerializer
# from api.serializers import ReviewsSerializer
# from api.serializers import CommentsSerializer
from api.serializers import UsersSerializer


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
