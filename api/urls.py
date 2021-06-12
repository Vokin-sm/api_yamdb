from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (TitlesViewSet, CategoriesViewSet,
                       GenresViewSet, ReviewsViewSet,
                       CommentsViewSet, UsersViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    'v1/titles',
    TitlesViewSet,
    basename='titles'
)
router_v1.register(
    'v1/categories',
    CategoriesViewSet,
    basename='categories'
)
router_v1.register(
    'v1/genres',
    GenresViewSet,
    basename='genres'
)
router_v1.register(
    'v1/titles/(?P<title_id>[^/D+]+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    'v1/titles/(?P<title_id>[^/D+]+)/reviews/(?P<review_id>[^/D+]+)/comments',
    CommentsViewSet,
    basename='comments'
)
router_v1.register(
    'v1/users',
    UsersViewSet,
    basename='users'
)


urlpatterns = [
    path(
        '',
        include(router_v1.urls)
    ),
]