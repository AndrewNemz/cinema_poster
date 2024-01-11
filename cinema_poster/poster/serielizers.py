from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django.shortcuts import get_object_or_404
from poster.models import Tag, Genre, MovieRate, Cinema, Movie, CinemaMovies


class TagSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для тэгов.
    '''
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для жанров.
    '''
    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'slug',
        )


class MoviesInCinemaSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для фильмов, которые показываются в кинотеатре.
    id - PrimaryKeyRelatedField для того, чтобы сериализатор не терял id.
    для метода create CinemasSerializer.
    '''

    id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Movie
        fields = (
            'id',
            'name',
        )


class ShowCinemaMovies(serializers.ModelSerializer):
    pass


class CinemasSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для кинотеатров.
    '''

    movies = MoviesInCinemaSerializer(many=True, required=False)

    class Meta:
        model = Cinema
        fields = (
            'id',
            'name',
            'adress',
            'movies',
            'web_site',
        )

    @staticmethod
    def create_movies(movies, cinema):
        movies_list = []
        for movie in movies:
            movies_list.append(
                CinemaMovies(
                    movie=movie['id'], cinema=cinema
                )
            )
        CinemaMovies.objects.bulk_create(movies_list)

    def create(self, validated_data):
        movies = validated_data.pop('movies')
        cinema = Cinema.objects.create(**validated_data)
        self.create_movies(movies, cinema)
        return cinema
    
    def to_representation(self, instance):
        pass

    def update(self, instance, validated_data):
        pass
