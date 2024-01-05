import csv

from django.core.management import BaseCommand

from poster.models import Genre


class Command(BaseCommand):
    """
    Наполнение базы данных данными из data/genres.csv.
    Команда - python manage.py fill_db_genres
    """
    def handle(self, *args, **options):

        file_path = 'data/genres.csv'
        print('Загрузка началась')

        with open(file_path, 'r', encoding='utf-8') as csv_file:
            genres = csv.reader(csv_file)

            for row in genres:
                name, slug = row
                Genre.objects.get_or_create(
                    name=name,
                    slug=slug,
                )

        print('Загрузка успешно завершена')