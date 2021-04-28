from django.core.management.base import BaseCommand, CommandError
from foodster.recipes.models import Ingredient
import csv
import logging

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        with open('recipes/data/ingredients.csv') as file:
            file_reader = csv.reader(file)
            ingredient_count = 0
            for ingredient_count, row in enumerate(file_reader):
                name, unit = row
                Ingredient.objects.get_or_create(name=name, units=unit)
                
            logging.info(f'{ingredient_count} ingredients added.')
