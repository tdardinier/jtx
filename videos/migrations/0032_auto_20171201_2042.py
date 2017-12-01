# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0031_auto_20171118_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jtx',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('promo', models.IntegerField()),
                ('devise', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ['titre_playlist'],
            },
        ),
        migrations.CreateModel(
            name='Titreplaylist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=1000)),
            ],
            options={
                'ordering': ['label'],
            },
        ),
        migrations.AlterField(
            model_name='video',
            name='subtitles',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='titreplaylist',
            name='last_video',
            field=models.ForeignKey(blank=True, to='videos.Video', null=True),
        ),
        migrations.AddField(
            model_name='playlist',
            name='titre_playlist',
            field=models.ForeignKey(related_name='titre_playlist', to='videos.Titreplaylist'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='video_precedente',
            field=models.ForeignKey(related_name='video_precedente', to='videos.Video'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='video_suivante',
            field=models.ForeignKey(related_name='video_suivante', to='videos.Video'),
        ),
    ]
