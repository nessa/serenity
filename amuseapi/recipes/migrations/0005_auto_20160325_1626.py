# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipe_average_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='surname',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='language',
            field=models.CharField(default='es', choices=[('es', 'Español'), ('en', 'English')], max_length=10),
        ),
    ]
