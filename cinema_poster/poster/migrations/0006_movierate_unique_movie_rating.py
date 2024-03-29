# Generated by Django 3.2 on 2024-01-29 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poster', '0005_movierate_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='movierate',
            constraint=models.UniqueConstraint(fields=('movie', 'user'), name='unique_movie_rating'),
        ),
    ]
