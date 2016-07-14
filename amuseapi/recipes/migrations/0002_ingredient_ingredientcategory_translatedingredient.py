# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('code', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('ingredient', models.ForeignKey(to='recipes.Ingredient', related_name='categories')),
            ],
        ),
        migrations.CreateModel(
            name='TranslatedIngredient',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('translation', models.CharField(max_length=100)),
                ('language', models.CharField(choices=[('es', 'Español'), ('en', 'English')], default='es', max_length=10)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('ingredient', models.ForeignKey(to='recipes.Ingredient', related_name='translations')),
            ],
        ),
    ]
