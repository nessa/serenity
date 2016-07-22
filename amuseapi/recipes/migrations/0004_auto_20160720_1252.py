# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import models, migrations


def load_groups_fixture(apps, schema_editor):
    call_command('loaddata', 'groups_initial_data', app_label='recipes')

def load_users_fixture(apps, schema_editor):
    call_command('loaddata', 'users_initial_data', app_label='recipes')

def load_ingredients_fixture(apps, schema_editor):
    call_command('loaddata', 'ingredients_initial_data', app_label='recipes')

class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20160720_1252'),
    ]
    
    operations = [
        migrations.RunPython(load_groups_fixture),
        migrations.RunPython(load_users_fixture),
        migrations.RunPython(load_ingredients_fixture),
    ]
