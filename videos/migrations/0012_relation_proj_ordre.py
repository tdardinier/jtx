# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0011_implique'),
    ]

    operations = [
        migrations.AddField(
            model_name='relation_proj',
            name='ordre',
            field=models.IntegerField(default=0),
        ),
    ]
