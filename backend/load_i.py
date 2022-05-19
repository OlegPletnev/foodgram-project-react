import csv

from recipes.models import Ingredient

with open('ingredients.csv', 'r', encoding='UTF-8') as file:
    reader = csv.reader(file)
    for row in reader:
        # if len(row) == 2:
        Ingredient.objects.get_or_create(name=row[0], measurement_unit=row[1],)

Ingredient.objects.bulk_create(Ingredient(**tag) for tag in reader)
