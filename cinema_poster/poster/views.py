from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import (SAFE_METHODS, AllowAny,
                                        IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly)
from poster.models import Tag, Genre, Cinema, Movie, MovieRate
from poster.serielizers import TagSerializer, GenreSerializer, CinemasSerializer, MoviesSerializer, RatingSerializer
from poster.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class TagsViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с тегами.
    Запросы доступны только администраторам.
    """
    queryset = Tag.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = TagSerializer
    pagination_class = None


class GenresViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с тегами.
    Запросы доступны только администраторам.
    """
    queryset = Genre.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = GenreSerializer
    pagination_class = None


class CinemasViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для работы с кинотеатрами.
    Списки кинотеатров доступны всем.
    Post запросы только для admin.
    '''
    
    queryset = Cinema.objects.all()
    serializer_class = CinemasSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class MoviesViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для работы с фильмами.
    Списки кинотеатров доступны всем.
    Post запросы только для admin.
    '''
    
    queryset = Movie.objects.all()
    serializer_class = MoviesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class RatingViewSet(viewsets.ModelViewSet):
    '''
    Сериализатор для рейтинга фильма.
    Ставить оценку фильма может только зарегестрированный пользователь.
    '''

    queryset = MovieRate.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    pagination_class = None

    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('movie_id'))
        serializer.save(user=self.request.user, movie=movie)

    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('movie_id'))
        return movie.movie_rate.all()