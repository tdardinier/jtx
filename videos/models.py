from __future__ import unicode_literals
import datetime

from django.contrib.auth.models import User
from django.db import models

class Video(models.Model):
    titre = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)
    url = models.CharField(max_length=1000)
    views = models.IntegerField(default=0)
    public = models.BooleanField(default=False)
    duree = models.IntegerField(default=0)
    description = models.CharField(max_length=1000, default="Pas de description disponible.")
    def __unicode__(self):
        return self.titre

class Tag(models.Model):
    titre = models.CharField(max_length=100)
    def __unicode__(self):
        return self.titre

class Implique(models.Model):
    grand = models.ForeignKey(Tag, related_name="grand")
    petit = models.ForeignKey(Tag, related_name="petit")
    def __unicode__(self):
        return self.petit.titre + " => " + self.grand.titre

class Category(models.Model):
    titre = models.CharField(max_length=100)
    public = models.BooleanField(default=False)
    def __unicode__(self):
        return self.titre

class Proj(models.Model):
    titre = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    date = models.DateField(default=datetime.date.today)
    views = models.IntegerField(default=0)
    image = models.CharField(max_length=2000, default="http://cdn.wallpapersafari.com/58/12/nyHXSO.jpg")
    def __unicode__(self):
        return self.titre

class Favorite(models.Model):
    user = models.ForeignKey(User)
    video = models.ForeignKey(Video)
    date = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = (('user', 'video'),)

    def __unicode__(self):
        return self.user.username + " : " + self.video.titre

class Relation_proj(models.Model):
    class Meta:
        ordering = ['ordre']
    proj = models.ForeignKey(Proj)
    video = models.ForeignKey(Video)
    ordre = models.IntegerField(default=0)
    def __unicode__(self):
        return self.proj.titre + u" : " + self.video.titre

class Relation_tag(models.Model):
    tag = models.ForeignKey(Tag)
    video = models.ForeignKey(Video)
    def __unicode__(self):
        return self.video.titre + u" : " + self.tag.titre

class Relation_comment(models.Model):
    comment = models.CharField(max_length=1000)
    video = models.ForeignKey(Video)
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User)
    def __unicode__(self):
        return self.video.titre + u" : " + self.comment

class Relation_comment_proj(models.Model):
    comment = models.CharField(max_length=1000)
    proj = models.ForeignKey(Proj)
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User)
    def __unicode__(self):
        return self.proj.titre + u" : " + self.comment
