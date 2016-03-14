# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_reciperating'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='comments_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='total_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='users_rating',
            field=models.IntegerField(default=0),
        ),
    ]
