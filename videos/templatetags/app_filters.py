from django import template
from django.urls import reverse
from videos.models import Relation_proj
from django.shortcuts import render, get_object_or_404

register = template.Library()

@register.filter(name='duration')
def duration(v):
    return '{:01}'.format(v.duree // 60) + ':' + '{:02}'.format(v.duree % 60)

@register.filter(name='auteurs')
def auteurs(v):
    s = v.relation_auteur_video_set.all()
    if len(s) > 0:
        return ", ".join(["<a style='color:black;' href='" + reverse('jtxman', args=(x.auteur.id,1,)) + "'>"
            + x.auteur.name + "</a>" for x in s])
    else:
        return "Auteur inconnu"

@register.filter(name='url_auteur')
def url_auteur(a):
    return reverse('jtxman', args=(a.id,1,))

@register.filter(name='short')
def short(s):
    n = 70
    if len(s) <= n:
        return s
    else:
        return s[:(n - 3)] + "..."

@register.filter(name='short_promo')
def short_promo(e):
    return str(e.promo)[-2:]

@register.filter(name='duration_proj')
def duration(p):
    s = 0
    for r in p.relation_proj_set.all():
        s += r.video.duree
    c = '{:02}'.format(s % 60)
    s //= 60
    b = '{:02}'.format(s % 60)
    a = str(s // 60)
    return a + ":" + b + ":" + c

@register.filter(name='duration_proj_seconds')
def duration_sec(p):
    s = 0
    for r in p.relation_proj_set.all():
        s += r.video.duree
    return s

@register.filter(name='exists_user')
def exists_user(elements, user):
    return elements.filter(user = user).exists()

@register.filter(name='get_promo_video')
def get_promo_video(video,typ):
    r=Relation_proj.objects.get(video=video)
    if r:
        if typ=='short':
            return str(r.proj.promo)[-2:]
        else:
            return str(r.proj.promo)
    else:
        return "INC"

@register.filter(name='get_percent')
def get_percent(video,proj_duree):
    s = 0
    return 100.0*video.duree/(proj_duree+0.0)

@register.filter(name='get_list')
def get_list(name):
    from videos.models import Category
    if name=='categories':
        return  Category.objects.all()

@register.filter(name='replace_opacity')
def replace_opacity(color_string,opa):
    l=color_string.split(',')
    l[-1]=opa+')'
    return ','.join(l)

@register.filter(name='get_jaime')
def get_jaime(proj):
    from videos.models import Favorite_proj
    return Favorite_proj.objects.filter(proj = proj).count()