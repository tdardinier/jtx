# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-20 20:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0021_auto_20170620_2035'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='also_favorite',
            new_name='epingle',
        ),
        migrations.RenameField(
            model_name='favorite_proj',
            old_name='also_favorite',
            new_name='epingle',
        ),
    ]