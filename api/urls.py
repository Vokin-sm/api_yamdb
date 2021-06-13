from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (TitlesViewSet, CategoriesViewSet,
                       GenresViewSet, ReviewsViewSet,
                       CommentsViewSet, UsersViewSet)

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
]
