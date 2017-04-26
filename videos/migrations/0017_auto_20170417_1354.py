# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0016_auteur_relation_auteur_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite_proj',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='proj',
            options={'ordering': ['-promo', '-date']},
        ),
        migrations.AddField(
            model_name='proj',
            name='promo',
            field=models.IntegerField(default=2015),
        ),
        migrations.AlterUniqueTogether(
            name='relation_auteur_video',
            unique_together=set([('video', 'auteur')]),
        ),
        migrations.AlterUniqueTogether(
            name='relation_proj',
            unique_together=set([('proj', 'video')]),
        ),
        migrations.AlterUniqueTogether(
            name='relation_tag',
            unique_together=set([('tag', 'video')]),
        ),
        migrations.AddField(
            model_name='favorite_proj',
            name='proj',
            field=models.ForeignKey(to='videos.Proj'),
        ),
        migrations.AddField(
            model_name='favorite_proj',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='favorite_proj',
            unique_together=set([('user', 'proj')]),
        ),
    ]
