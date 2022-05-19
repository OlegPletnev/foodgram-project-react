from _csv import reader
from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """Загрузка инградиентов в одноименную таблицу БД."""
    help = "Загрузка данных из csv-файла."

    def handle(self, *args, **kwargs):
        with open('ingredients.csv', 'r', encoding='UTF-8') as file:
            for row in reader(file):
                if len(row) == 2:
                    Ingredient.objects.get_or_create(
                        name=row[0], measurement_unit=row[1],
                    )
