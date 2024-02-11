# Generated by Django 3.2 on 2024-02-11 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poster', '0007_auto_20240205_1759'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='movierate',
            name='unique_movie_rating',
        ),
        migrations.AddConstraint(
            model_name='movierate',
            constraint=models.UniqueConstraint(fields=('movie', 'user', 'rating'), name='unique_movie_rating'),
        ),
    ]