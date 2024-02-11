from django.contrib import admin

from .models import (Cinema, CinemaMovies, FavoriteMovie, Genre, Movie,
                     MovieRate, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'tag',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'web_site',
        'adress',
    )
    search_fields = ('name', 'adress')
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(CinemaMovies)
class CinemaMoviesAdmin(admin.ModelAdmin):
    list_display = (
        'movie',
        'cinema',
    )


@admin.register(MovieRate)
class MovieRateAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'movie',
        'rating',
    )


@admin.register(FavoriteMovie)
class FavoriteMovieAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'movie',
    )
