# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0012_relation_proj_ordre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relation_proj',
            options={'ordering': ['ordre']},
        ),
    ]
