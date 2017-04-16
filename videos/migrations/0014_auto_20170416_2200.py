# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0013_auto_20170416_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='description',
            field=models.CharField(default='Pas de description disponible.', max_length=1000),
        ),
        migrations.AddField(
            model_name='video',
            name='duree',
            field=models.IntegerField(default=0),
        ),
    ]
