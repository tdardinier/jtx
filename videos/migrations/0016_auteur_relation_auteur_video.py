# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0015_auto_20170417_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auteur',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('promo', models.IntegerField(default=2015)),
            ],
        ),
        migrations.CreateModel(
            name='Relation_auteur_video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auteur', models.ForeignKey(to='videos.Auteur')),
                ('video', models.ForeignKey(to='videos.Video')),
            ],
        ),
    ]
