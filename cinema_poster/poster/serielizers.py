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

    id = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())

    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
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

    def validate(self, data):
        movies = data['movies']
        movies_list = []
        for movie in movies:
            if movie in movies_list:
                raise serializers.ValidationError(
                    {
                        'movies': f'В базе кинотеатра уже есть фильм {movie["name"]}'
                    }
                )
            movies_list.append(movie)
        return data
    
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

    def update(self, instance, validated_data):
        CinemaMovies.objects.filter(cinema=instance).delete()
        self.create_movies(validated_data.pop('movies'), instance)
        return super().update(instance, validated_data)


class MoviesSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для создания фильмов.
    '''

    genre = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Movie
        fields = (
            'id',
            'name',
            'author',
            'actors',
            'tag',
            'genre',
        )

    def validate(self, data):
        genre = data['genre']
        genres_list = []
        if not genre:
            raise serializers.ValidationError(
                {
                    'genre': 'У фильма должен быть жанр.'
                }
            )
        for gen in genre:
            if gen in genres_list:
                raise serializers.ValidationError(
                {
                    'genre': 'У фильма уже есть такой жанр.'
                }
            )
            genres_list.append(gen)
        return data

    @staticmethod
    def create_genres(genres, movie):
        for genre in genres:
            movie.genre.add(genre)

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        movie = Movie.objects.create(**validated_data)
        self.create_genres(genres, movie)
        return movie

    def update(self, instance, validated_data):
        instance.genre.clear()
        self.create_genres(validated_data.pop('genre'), instance)
        return super().update(instance, validated_data)
    
    '''def to_representation(self, instance):
        pass'''
