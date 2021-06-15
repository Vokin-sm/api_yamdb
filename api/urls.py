from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import (TitlesViewSet, CategoriesViewSet,
                       GenresViewSet, ReviewsViewSet,
                       CommentsViewSet, UsersViewSet,
                       UsersMeAPIView)

router_v1 = DefaultRouter()
router_v1.register(
    'titles',
    TitlesViewSet,
    basename='titles'
)
router_v1.register(
    'categories',
    CategoriesViewSet,
    basename='categories'
)
router_v1.register(
    'genres',
    GenresViewSet,
    basename='genres'
)
router_v1.register(
    'titles/(?P<title_id>[^/D+]+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    'titles/(?P<title_id>[^/D+]+)/reviews/(?P<review_id>[^/D+]+)/comments',
    CommentsViewSet,
    basename='comments'
)
router_v1.register(
    'users',
    UsersViewSet,
    basename='users'
)

urlpatterns = [
    path(
        'v1/users/me/',
        UsersMeAPIView.as_view(),
        name='users_me'
    ),
    path(
        'v1/',
        include(router_v1.urls)
    ),
    # path(
    #     'v1/auth/',
    #     include('djoser.urls')
    # ),
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
