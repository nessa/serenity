# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management import call_command
from django.db import models, migrations

fixture = 'initial_data'

def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture, app_label='recipes')
    
class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20160720_1147'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
