# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logreg', '0007_auto_20170629_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poke',
            name='counter',
            field=models.IntegerField(),
        ),
    ]
