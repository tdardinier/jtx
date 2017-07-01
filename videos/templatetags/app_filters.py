from django import template
from django.urls import reverse

register = template.Library()

@register.filter(name='duration')
def duration(v):
    return '{:01}'.format(v.duree // 60) + ':' + '{:02}'.format(v.duree % 60)

@register.filter(name='auteurs')
def auteurs(v):
    s = v.relation_auteur_video_set.all()
    if len(s) > 0:
        return ", ".join(["<a href='" + reverse('jtxman', args=(x.auteur.id,1,)) + "'>"
            + x.auteur.name + "</a>" for x in s])
    else:
        return "Inconnu"

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
