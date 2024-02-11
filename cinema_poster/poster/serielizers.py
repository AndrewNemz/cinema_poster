from django.db.models import Avg
from rest_framework import serializers

from poster.models import (Cinema, CinemaMovies, FavoriteMovie, Genre, Movie,
                           MovieRate, Tag)


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
                        'movies': f'В кинотеатра есть фильм {movie["name"]}'
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


class ShowMovieSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для отображения информации о фильме.
    '''

    rating = serializers.SerializerMethodField(read_only=True)
    tag = serializers.StringRelatedField(read_only=True)
    genre = serializers.StringRelatedField(read_only=True, many=True)
    is_favorite = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id',
            'name',
            'author',
            'actors',
            'genre',
            'tag',
            'rating',
            'is_favorite',
        )

    def get_rating(self, obj):
        return obj.movie_rate.all().aggregate(Avg('rating'))

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite.filter(movie=obj).exists()


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

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowMovieSerializer(instance, context=context).data


class ShowFavoriteSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для отображения избранных фильмов.
    '''

    movie = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = FavoriteMovie
        fields = (
            'id',
            'user',
            'movie',
        )


class ShowRatingSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для отображения рейтинга фильма.
    '''

    movie = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = MovieRate
        fields = (
            'id',
            'movie',
            'user',
            'rating',
        )


class RatingSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для рейтинга фильма.
    '''

    class Meta:
        model = MovieRate
        fields = (
            'id',
            'movie',
            'rating',
        )

    def validate(self, data):
        movie = data['movie']
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        if MovieRate.objects.filter(
            movie=movie,
            user=request.user,
        ).exists():
            raise serializers.ValidationError(
                {
                    'status': 'Вы уже ставили такую оценку фильму.'
                }
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowRatingSerializer(instance, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для избранных фильмов.
    '''

    class Meta:
        model = FavoriteMovie
        fields = (
            'id',
            'user',
            'movie'
        )

    def validate(self, data):
        movie = data['movie']
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        if FavoriteMovie.objects.filter(
            movie=movie,
            user=request.user
        ).exists():
            raise serializers.ValidationError(
                {
                    'status': 'Вы уже добавили фильм в избранные.'
                }
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowFavoriteSerializer(instance, context=context).data
