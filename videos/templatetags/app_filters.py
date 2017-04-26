from django import template

register = template.Library()

@register.filter(name='duration')
def duration(v):
    return '{:01}'.format(v.duree // 60) + ':' + '{:02}'.format(v.duree % 60)

@register.filter(name='auteurs')
def auteurs(v):
    s = v.relation_auteur_video_set.all()
    if len(s) > 0:
        return ", ".join([x.auteur.name for x in s])
    else:
        return "Inconnu"

@register.filter(name='short')
def short(s):
    n = 25
    if len(s) <= n:
        return s
    else:
        return s[:(n - 3)] + "..."
