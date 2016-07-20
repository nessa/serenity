# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import models, migrations

fixture = 'groups_initial_data'

def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture, app_label='recipes')
        
class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_ingredient_ingredientcategory_translatedingredient'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
