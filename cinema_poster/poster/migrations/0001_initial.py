# Generated by Django 3.2 on 2024-01-05 13:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название кинотеатра')),
                ('adress', models.TextField(unique=True, verbose_name='Адресс кинотеатра')),
                ('web_site', models.URLField(max_length=256, unique=True, verbose_name='Сайт кинотеатра')),
            ],
            options={
                'verbose_name': 'Кинотеатр',
                'verbose_name_plural': 'Кинотеатры',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, unique=True, verbose_name='Название фильма')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('0+', '0+'), ('6+', '6+'), ('12+', '12+'), ('16+', '16+'), ('18+', '18+')], default='0+', max_length=16, unique=True, verbose_name='Название тэга')),
                ('color', models.CharField(max_length=7, unique=True, validators=[django.core.validators.RegexValidator(message='Введенное значение не является цветом в формате HEX.', regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')], verbose_name='Цвет тэга HEX формата')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг тэга')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=256, unique=True, verbose_name='Название фильма')),
                ('author', models.CharField(max_length=256, verbose_name='Режиссер')),
                ('actors', models.TextField(max_length=256, verbose_name='Актеры фильма')),
                ('genre', models.ManyToManyField(related_name='movies', to='poster.Genre', verbose_name='Жанры фильма')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='poster.tag', verbose_name='Тэг фильма')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
                'ordering': ['-name', '-author'],
            },
        ),
        migrations.CreateModel(
            name='CinemaRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минималная оценка фильма - 1'), django.core.validators.MaxValueValidator(10, message='Максимальная оценка фильма - 10')], verbose_name='Score')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_rate', to='poster.movie', verbose_name='фильм')),
            ],
            options={
                'verbose_name': 'Рейтинг фильма',
                'verbose_name_plural': 'Рейтинги фильмов',
            },
        ),
        migrations.CreateModel(
            name='CinemaMovies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movies_in_cinema', to='poster.cinema', verbose_name='Кинотеатр')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movies_in_cinema', to='poster.movie', verbose_name='Фильм')),
            ],
            options={
                'verbose_name': 'Фильм в кинотеатре',
                'verbose_name_plural': 'Фильмы в кинотеатре',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='cinema',
            name='movies',
            field=models.ManyToManyField(related_name='cinemas', through='poster.CinemaMovies', to='poster.Movie', verbose_name='Кинофильмы'),
        ),
        migrations.AddConstraint(
            model_name='cinemamovies',
            constraint=models.UniqueConstraint(fields=('movie', 'cinema'), name='unique_movie'),
        ),
    ]