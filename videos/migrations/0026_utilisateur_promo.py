# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0025_auto_20170702_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='promo',
            field=models.IntegerField(default=0),
        ),
    ]
