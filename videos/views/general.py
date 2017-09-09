#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse

import random
from os import listdir

from .edit import *
from .search import *
from .autoproj import *
from .likes import *
from .connection import *

n_page = 36
n_index = 12
n_suggestions = 12

def jtxman(request, auteur_id, page=1):
    man = get_object_or_404(Auteur, pk=auteur_id)
    videos = filter_relation(request, man.relation_auteur_video_set)
    context = {
        'titre': "JTXman " + str(man.promo) + " : " + man.firstname + " " + man.lastname,
        'id': auteur_id,
    }
    return pagination(request, 'videos.html', context, videos, page, 'jtxman', lambda x: x.video)

def id(x):
    return x

def index(request):
    projs = filter(request, Proj.objects)
    videos = filter(request, Video.objects)
    categories = filter_category(request, Category.objects)
    context = {
        'request': request,
        'projs': projs.all()[:n_index],
        'videos': videos.all().order_by('?')[:n_index],
        'categories': categories.all(),
    }
    return render(request, 'index.html', context)

def jtx(request, year):
    c = Category.objects.get(titre="Proj en .K")
    v = filter(request, Proj.objects.filter(promo=year))
    context = {
        'year': year,
        'projs_jtx': v.filter(category=c),
        'projs_autres': v.exclude(category=c),
        'jtxmen': Auteur.objects.filter(promo=year),
        'videos': Video.objects.order_by('-views')[:12]
    }
    return render(request, 'jtx.html', context)

def categories(request):
    categories = filter_category(request, Category.objects)
    context = {
        'categories': categories.all(),
    }
    return render(request, 'categories.html', context)

def pagination(request, template, context, elements, page, adress, f = id):
    page = int(page)
    nb_page = ((elements.count() - 1) // n_page) + 1
    elements = elements.all()[(page - 1) * n_page:page * n_page]
    context['pages'] = range(1, nb_page + 1)
    context['page'] = page
    elements = map(f, elements)
    context['elements'] = elements
    context['adress'] = adress
    return render(request, template, context)

def category(request, category_id, page=1):
    cat = get_object_or_404(Category, pk=category_id)
    if cat.public or request.user.is_authenticated:
        projs = Proj.objects.filter(category=cat)
        context = {
            'titre': cat.titre,
            'id': category_id,
        }
        return pagination(request, 'projs.html', context, projs, page, 'category')
    else:
        return index(request)

def projs(request, page=1):
    projs = filter(request, Proj.objects)
    context = {
        'titre': 'Toutes les projs visibles',
    }
    return pagination(request, 'projs.html', context, projs, page, 'projs')

#AJOUT VIDON
def fil(request, page=1):
    projs = filter(request, Proj.objects)
    c = Category.objects.get(titre="Proj en .K")
    context = {
        'titre': 'Toutes les projs visibles',
        'projs_jtx': projs.filter(category=c),
    }
    return pagination(request, 'fil_temporel.html', context, projs, page, 'projs')

def proj(request, proj_id):
    proj = get_object_or_404(Proj, pk=proj_id)
    if proj.category.public or request.user.is_authenticated:
        n = Favorite_proj.objects.filter(proj = proj).count()
        favorite = False
        epingle = False
        all_projs = filter(request, Proj.objects)
        if request.user.is_authenticated:
            user = request.user
            favorite = Favorite_proj.objects.filter(user = user, proj = proj).exists()
            epingle = Favorite_proj.objects.filter(user = user, proj = proj, epingle = True).exists()
        suggestions = all_projs.all().order_by('?')[:n_suggestions]
        proj.views += 1
        proj.save()
        context = {
            'can_proj': can_proj(request),
            'proj': proj,
            'suggestions': suggestions,
            'favorite': favorite,
            'epingle': epingle,
            'nb_jaimes': n,
        }
        return render(request, 'proj_new.html', context)
    return index(request)

def favorites(request, page=1):
    if (request.user.is_authenticated):
        user = request.user
        favorites = Favorite.objects.filter(user = user)
        context = {
            'titre': 'Vidéos aimées',
        }
        return pagination(request, 'videos.html', context, favorites, page, 'favorites', lambda x: x.video)
    else:
        return index(request)

def videos(request, page=1):
    videos = filter(request, Video.objects)
    context = {
        'titre': 'Toutes les vidéos',
    }
    return pagination(request, 'videos.html', context, videos, page, 'videos')

def video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if video.category.public or request.user.is_authenticated:
        video.views += 1
        video.save()
        n = Favorite.objects.filter(video = video).count()
        favorite = False
        epingle = False
        all_videos = filter(request, Video.objects)
        if request.user.is_authenticated:
            user = request.user
            favorite = Favorite.objects.filter(user = user, video = video).exists()
            epingle = Favorite.objects.filter(user = user, video = video, epingle = True).exists()
        suggestions = all_videos.all().order_by('?')[:n_suggestions]
        context = {
            'can_edit': can_edit(request),
            'video': video,
            'suggestions': suggestions,
            'favorite': favorite,
            'epingle': epingle,
            'nb_jaimes': n,
        }
        return render(request, 'video.html', context)
    return index(request)

def tags(request):
    tags = Tag.objects.all()
    context = {
        'tags': tags,
    }
    return render(request, 'tags.html', context)

def tag(request, tag_id, page=1):
    tag = get_object_or_404(Tag, pk=tag_id)
    videos = filter_relation(request, tag.relation_tag_set)
    context = {
        'titre': tag.titre,
        'titre_tag': True,
        'id': tag_id,
    }
    return pagination(request, 'videos.html', context, videos, page, 'tag', lambda x: x.video)

def comment_video(request, video_id):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, pk=video_id)
        comment = request.POST['comment']
        user = request.user
        c = Relation_comment(author = user, video = video, comment = comment)
        c.save()
    return HttpResponseRedirect(reverse('video', args=(video.id,)))

def comment_proj(request, proj_id):
    if request.user.is_authenticated:
        proj = get_object_or_404(Proj, pk=proj_id)
        comment = request.POST['comment']
        user = request.user
        c = Relation_comment_proj(author = user, proj = proj, comment = comment)
        c.save()
    return HttpResponseRedirect(reverse('proj', args=(proj.id,)))

def delete_comment_video(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Relation_comment, pk=comment_id)
        user = request.user
        if user == comment.author:
            comment.delete()
    return HttpResponseRedirect(reverse('video', args=(comment.video.id,)))

def delete_comment_proj(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Relation_comment_proj, pk=comment_id)
        user = request.user
        if user == comment.author:
            comment.delete()
    return HttpResponseRedirect(reverse('proj', args=(comment.proj.id,)))




