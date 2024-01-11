from django.db import models
from django.core import validators


class Tag(models.Model):
    '''
    Модель для тегов.
    Цвет тэгов обязательно в HEX формате.
    '''

    TAG_CHOICES = (
        ('0+', '0+'),
        ('6+', '6+'),
        ('12+', '12+'),
        ('16+', '16+'),
        ('18+', '18+'),
    )
    name = models.CharField(
        verbose_name='Название тэга',
        max_length=16,
        unique=True,
        choices=TAG_CHOICES,
        default='0+',
    )
    color = models.CharField(
        verbose_name='Цвет тэга HEX формата',
        unique=True,
        max_length=7,
        validators=[
            validators.RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введенное значение не является цветом в формате HEX.'
            )
        ]
    )
    slug = models.SlugField(
        verbose_name='Слаг тэга',
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name
    

class Genre(models.Model):
    '''
    Модель для жанра фильма.
    '''

    name = models.CharField(
        verbose_name='Название фильма',
        unique=True,
        max_length=24,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        max_length=50,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name
        

class Movie(models.Model):
    '''
    Модель для информации и фильме.    
    '''

    name = models.TextField(
        verbose_name='Название фильма',
        max_length=256,
    )
    author = models.CharField(
        verbose_name='Режиссер',
        max_length=256,
    )
    actors = models.TextField(
        verbose_name='Актеры фильма',
        max_length=256,
    )
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тэг фильма',
        related_name='movies',
        on_delete=models.CASCADE,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры фильма',
        related_name='movies',
    )

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['-name', '-author',]

    def __str__(self):
        return self.name


class Cinema(models.Model):
    '''
    Модель для информации и кинотеатре.
    '''

    name = models.CharField(
        verbose_name='Название кинотеатра',
        unique=True,
        max_length=50,
    )
    adress = models.TextField(
        verbose_name='Адресс кинотеатра',
        unique=True,
    )
    movies = models.ManyToManyField(
        Movie,
        through='CinemaMovies',
        verbose_name='Кинофильмы',
        related_name='cinemas',
    )
    web_site = models.URLField(
        verbose_name='Сайт кинотеатра',
        max_length=256,
        unique=True,
    )

    class Meta:
        verbose_name='Кинотеатр'
        verbose_name_plural='Кинотеатры'
        ordering = ['-name',]

    def __str__(self):
        return self.name


class CinemaMovies(models.Model):
    '''
    Модель для информации о фильмах в кинотеатре.
    '''

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name='Фильм',
        related_name='movies_in_cinema',
    )
    cinema = models.ForeignKey(
        Cinema,
        on_delete=models.CASCADE,
        verbose_name='Кинотеатр',
        related_name='movies_in_cinema',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('movie', 'cinema',),
                name='unique_movie',
            ),
        )
        verbose_name = 'Фильм в кинотеатре'
        verbose_name_plural = 'Фильмы в кинотеатре'
        ordering = ['-id']

    def __str__(self):
        return self.movie.name


class MovieRate(models.Model):
    '''
    Модель для рейтинга фильмов.
    '''

    movie = models.ForeignKey(
        Movie,
        verbose_name='фильм',
        related_name='movie_rate',
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField(
        validators=[
            validators.MinValueValidator(
                1,
                message='Минималная оценка фильма - 1'
            ),
            validators.MaxValueValidator(
                10,
                message='Максимальная оценка фильма - 10'
            )
        ],
        verbose_name='Score'
    )

    class Meta:
        verbose_name = 'Рейтинг фильма'
        verbose_name_plural = 'Рейтинги фильмов'

    def __str__(self):
        return self.movie.name
