from django import template

register = template.Library()

@register.filter(name='duration')
def duration(v):
    return str(v.duree // 60) + ':' + str(v.duree % 60)

