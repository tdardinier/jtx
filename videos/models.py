from __future__ import unicode_literals
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DROITS = (
        ('0', 'admin'),
        ('1', 'jtxman'),
        ('2', 'etudiant'),
        ('3', 'dfhm'),
    )
    profil = models.CharField(max_length=1, choices=DROITS, default='2')
    promo = models.IntegerField(default=0)

    # Tags, auteurs
    @property
    def can_edit(self):
        return self.profil == '0' or self.profil == '1'

    # Add une proj, changer l'ordre, les titres
    @property
    def can_proj(self):
        return self.profil == '0'

    def __unicode__(self):
        return self.user.__unicode__() + u' -> ' + self.profil

#@receiver(post_save, sender=User)
#def create_utilisateur(sender, instance, created, **kwargs):
#    if created:
#        Utilisateur.objects.create(user=instance)

#@receiver(post_save, sender=User)
#def save_user_utilisateur(sender, instance, **kwargs):
#    instance.utilisateur.save()

class Category(models.Model):
    titre = models.CharField(max_length=100)
    public = models.BooleanField(default=False)
    def __unicode__(self):
        return self.titre

class Video(models.Model):
    class Meta:
        ordering = ['-date']
    titre = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)
    url = models.CharField(max_length=1000)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(Category)
    duree = models.IntegerField(default=0)

    description = models.CharField(max_length=1000, default="Pas de description disponible.")
    def __unicode__(self):
        return self.titre

class Auteur(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    promo = models.IntegerField(default=2015)

    @property
    def name(self):
        return self.firstname + " " + self.lastname

    def __unicode__(self):
        return self.name + "(JTX" + str(self.promo) + ")"

class Relation_auteur_video(models.Model):
    class Meta:
        unique_together = (('video', 'auteur'),)
    video = models.ForeignKey(Video)
    auteur = models.ForeignKey(Auteur)
    def __unicode__(self):
        return self.video.titre + " - " + self.auteur.name

class Tag(models.Model):
    titre = models.CharField(max_length=100)
    def __unicode__(self):
        return self.titre

class Implique(models.Model):
    grand = models.ForeignKey(Tag, related_name="grand")
    petit = models.ForeignKey(Tag, related_name="petit")
    def __unicode__(self):
        return self.petit.titre + " => " + self.grand.titre

class Proj(models.Model):
    class Meta:
        ordering = ['-promo', '-date']
    titre = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    date = models.DateField(default=datetime.date.today)
    promo = models.IntegerField(default=2015)
    views = models.IntegerField(default=0)
    description = models.CharField(max_length=1000, default="Pas de description disponible.")
    image = models.CharField(max_length=2000, default="http://cdn.wallpapersafari.com/58/12/nyHXSO.jpg")
    def __unicode__(self):
        return self.titre

class Favorite(models.Model):
    class Meta:
        ordering = ['-date']
        unique_together = (('user', 'video'),)
    epingle = models.BooleanField(default = False)
    user = models.ForeignKey(User)
    video = models.ForeignKey(Video)
    date = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return self.user.username + " : " + self.video.titre

class Favorite_proj(models.Model):
    class Meta:
        ordering = ['-date']
        unique_together = (('user', 'proj'),)
    epingle = models.BooleanField(default = False)
    user = models.ForeignKey(User)
    proj = models.ForeignKey(Proj)
    date = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return self.user.username + " : " + self.proj.titre

class Relation_proj(models.Model):
    class Meta:
        ordering = ['ordre']
        unique_together = (('proj', 'video'),)
    proj = models.ForeignKey(Proj)
    video = models.ForeignKey(Video)
    ordre = models.IntegerField(default=0)
    def __unicode__(self):
        return self.proj.titre + u" : " + self.video.titre

class Relation_tag(models.Model):
    class Meta:
        unique_together = (('tag', 'video'),)
    tag = models.ForeignKey(Tag)
    video = models.ForeignKey(Video)
    def __unicode__(self):
        return self.video.titre + u" : " + self.tag.titre

class Relation_comment(models.Model):
    class Meta:
        ordering = ['date']
    comment = models.CharField(max_length=1000)
    video = models.ForeignKey(Video)
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User)
    def __unicode__(self):
        return self.video.titre + u" : " + self.comment

class Relation_comment_proj(models.Model):
    class Meta:
        ordering = ['date']
    comment = models.CharField(max_length=1000)
    proj = models.ForeignKey(Proj)
    date = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User)
    def __unicode__(self):
        return self.proj.titre + u" : " + self.comment

class Like_comment(models.Model):
    class Meta:
        unique_together = (('user', 'comment'),)
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Relation_comment)
    date = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return self.user.username + " : " + self.comment.video.titre

class Like_comment_proj(models.Model):
    class Meta:
        unique_together = (('user', 'comment'),)
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Relation_comment_proj)
    date = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        return self.user.username + " : " + self.comment.proj.titre
