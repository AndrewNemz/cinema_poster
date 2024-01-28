from rest_framework.routers import DefaultRouter
from django.urls import include, path
from poster.views import TagsViewSet, GenresViewSet, CinemasViewSet, MoviesViewSet

app_name='poster'


router = DefaultRouter()
router.register('genres', GenresViewSet, basename='genres')
router.register('tags', TagsViewSet, basename='tags')
router.register('cinemas', CinemasViewSet, basename='cinemas')
router.register('movies', MoviesViewSet, basename='movies')


urlpatterns = [
    path('', include(router.urls)),
]
