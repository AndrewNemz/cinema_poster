from rest_framework import viewsets 
from rest_framework.permissions import (SAFE_METHODS, AllowAny,
                                        IsAuthenticated, IsAdminUser)
from poster.models import Tag, Genre, Cinema, Movie
from poster.serielizers import TagSerializer, GenreSerializer, CinemasSerializer, MoviesSerializer
from poster.permissions import IsAdminOrReadOnly


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
