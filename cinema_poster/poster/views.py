from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, AllowAny,
                                        IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly)
from poster.models import Tag, Genre, Cinema, Movie, MovieRate, FavoriteMovie
from poster.serielizers import TagSerializer, GenreSerializer, CinemasSerializer, MoviesSerializer, RatingSerializer, FavoriteSerializer, ShowMovieSerializer
from poster.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from poster.pagination import CustomPagination


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
    pagination_class = CustomPagination


class MoviesViewSet(viewsets.ModelViewSet):
    '''
    ViewSet для работы с фильмами.
    Списки кинотеатров доступны всем.
    Post запросы только для admin.
    '''

    serializer_class = MoviesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Movie.objects.all()
        is_favorite = self.request.query_params.get('is_favorite')
        if is_favorite is not None:
            queryset = queryset.filter(favorite=is_favorite)
        return queryset
    
    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'movie': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        movie = get_object_or_404(Movie, id=pk)
        model_obj = get_object_or_404(model, user=user, movie=movie)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request,
            pk=pk,
            serializers=FavoriteSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request,
            pk=pk,
            model=FavoriteMovie
        )


class RatingViewSet(viewsets.ModelViewSet):
    '''
    Сериализатор для рейтинга фильма.
    Ставить оценку фильма может только зарегестрированный пользователь.
    '''

    queryset = MovieRate.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('movie_id'))
        serializer.save(user=self.request.user, movie=movie)

    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs.get('movie_id'))
        return movie.movie_rate.all()
