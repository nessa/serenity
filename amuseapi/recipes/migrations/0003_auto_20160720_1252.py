# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_ingredient_ingredientcategory_translatedingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='measurement_unit',
            field=models.CharField(choices=[('g', 'gram'), ('kg', 'kilogram'), ('ml', 'milliliter'), ('l', 'liter'), ('pound', 'pound'), ('oz', 'ounce'), ('glass', 'glass'), ('unit', 'unit'), ('cup', 'cup'), ('tbsp', 'tablespoon'), ('tsp', 'teaspoon'), ('rasher', 'rasher'), ('stalk', 'stalk')], max_length=100, default='unit'),
        ),
    ]
