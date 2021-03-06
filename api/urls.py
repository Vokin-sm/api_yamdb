from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                       LoginView, ReviewsViewSet, TitlesViewSet, UsersViewSet,
                       send_confirmation_code_create_user)

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
        'v1/',
        include(router_v1.urls)
    ),
    path(
        'v1/auth/email/',
        send_confirmation_code_create_user,
        name='send_confirmation_code_create_user'
    ),
    path(
        'v1/auth/token/',
        LoginView.as_view(),
        name='login_view'
    ),
]
