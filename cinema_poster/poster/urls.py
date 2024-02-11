from django.urls import include, path
from rest_framework.routers import DefaultRouter

from poster.views import (CinemasViewSet, GenresViewSet, MoviesViewSet,
                          RatingViewSet, TagsViewSet)

app_name = 'poster'


router = DefaultRouter()
router.register('genres', GenresViewSet, basename='genres')
router.register('tags', TagsViewSet, basename='tags')
router.register('cinemas', CinemasViewSet, basename='cinemas')
router.register('movies', MoviesViewSet, basename='movies')
router.register(
    r'movies/(?P<movie_id>\d+)/rating',
    RatingViewSet,
    basename='rating'
)


urlpatterns = [
    path('', include(router.urls)),
]
