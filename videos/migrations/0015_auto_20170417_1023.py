# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0014_auto_20170416_2200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proj',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='relation_comment',
            options={'ordering': ['date']},
        ),
        migrations.AlterModelOptions(
            name='relation_comment_proj',
            options={'ordering': ['date']},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-date']},
        ),
    ]
