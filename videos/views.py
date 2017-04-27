#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import *

import random
from os import listdir

#from ffprobe import FFProbe

n_page = 30
n_index = 5
n_suggestions = 5

def can_proj(request):
    if request.user.is_authenticated:
        user = request.user
        return hasattr(user, 'utilisateur') and user.utilisateur.can_proj
    return False

def can_add_info(request):
    if request.user.is_authenticated:
        user = request.user
        return hasattr(user, 'utilisateur') and user.utilisateur.can_proj
    return False

def id(x):
    return x

def add_proj(request):

    context = {}

    if can_proj(request):

        base_url = "http://binet-jtx.com/videos"
        base_folder = "/nfs/serveur/ftp"
        extensions_acceptees = ['mp4', 'avi']

        p = request.POST
        if 'folder' in p and 'titre' in p:

            #folder = "Evenements/Amphi_presentation_binets/2016/MQ"
            #folder = "Evenements/Semaine_internationale/Houlgate_2017/MQ"
            #titre_proj = "Semaine internationale X2016 - Houlgate"

            folder = str(p['folder'])
            titre_proj = p['titre']

            c = Category.objects.get(pk = 10)
            p = Proj(titre = titre_proj, category = c)
            p.save()
            files = [str(f) for f in listdir(str(base_folder + "/" + folder)) if str(f)[-3:] in extensions_acceptees]
            files.sort()
            i = 1
            for f in files:
                base = '.'.join(f.split('.')[:-1])
                filename = str(base_folder + "/" + folder + "/" + f)
                #ld = FFProbe(filename).video
                ld = 0
                d = 0
                if len(ld) > 0:
                    dd = ld[0].duration
                    d = int(float(dd if dd != "N/A" else "0"))
                v = Video(titre = base.replace('_', ' '), url = base_url + "/" + folder + "/" + f, duree=d)
                v.save()
                r = Relation_proj(proj = p, video = v, ordre = i)
                r.save()
                i += 1
                context['message'] = u'Proj "' + titre_proj + u'" ajoutée avec succès !'
        else:
            context['message'] = "Version 1.0.17"
    else:
        context['message'] = "Vous ne pouvez pas !"
    return render(request, 'add_proj.html', context)

def index(request):
    projs = Proj.objects.filter(category__public=True)
    videos = Video.objects.filter(public=True)
    categories = Category.objects.filter(public=True)
    if (request.user.is_authenticated):
        projs = Proj.objects
        videos = Video.objects
        categories = Category.objects
    context = {
        'request': request,
        'projs': projs.all()[:n_index],
        'videos': videos.all().order_by('?')[:n_index],
        'categories': categories.all(),
    }
    return render(request, 'index.html', context)

def categories(request):
    categories = Category.objects.filter(public=True).all()
    if (request.user.is_authenticated):
        categories = Category.objects.all()
    context = {
        'categories': categories,
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
    projs = Proj.objects.filter(category__public=True)
    if (request.user.is_authenticated):
        projs = Proj.objects
    context = {
        'titre': 'Toutes les projs',
    }
    return pagination(request, 'projs.html', context, projs, page, 'projs')

def proj(request, proj_id):
    proj = get_object_or_404(Proj, pk=proj_id)
    if proj.category.public or request.user.is_authenticated:
        all_projs = Proj.objects.filter(category__public=True)
        if request.user.is_authenticated:
            all_projs = Proj.objects
        suggestions = all_projs.all().order_by('?')[:n_suggestions]
        proj.views += 1
        proj.save()
        context = {
            'proj': proj,
            'suggestions': suggestions,
        }
        return render(request, 'proj.html', context)
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
    videos = Video.objects.filter(public=True)
    if (request.user.is_authenticated):
        videos = Video.objects
    context = {
        'titre': 'Toutes les vidéos',
    }
    return pagination(request, 'videos.html', context, videos, page, 'videos')

def video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if video.public or request.user.is_authenticated:
        video.views += 1
        video.save()
        n = Favorite.objects.filter(video = video).count()
        favorite = False
        all_videos = Video.objects.filter(public=True)
        if request.user.is_authenticated:
            all_videos = Video.objects
            user = request.user
            favorite = Favorite.objects.filter(user = user, video = video).exists()
        suggestions = all_videos.all().order_by('?')[:n_suggestions]
        context = {
            'video': video,
            'suggestions': suggestions,
            'favorite': favorite,
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
    videos = tag.relation_tag_set.filter(video__public=True)
    if request.user.is_authenticated:
        videos = tag.relation_tag_set
    context = {
        'titre': tag.titre,
        'titre_tag': True,
        'id': tag_id,
    }
    return pagination(request, 'videos.html', context, videos, page, 'tag', lambda x: x.video)

def remove_favorite(request, video_id):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, pk=video_id)
        user = request.user
        c = Favorite.objects.filter(user = user, video = video).delete()
    return HttpResponseRedirect(reverse('video', args=(video.id,)))

def add_favorite(request, video_id):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, pk=video_id)
        user = request.user
        c = Favorite(user = user, video = video)
        c.save()
    return HttpResponseRedirect(reverse('video', args=(video.id,)))

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

def populate_bdd(request):
    #files = [f for f in listdir("/home/thibault/.banque/site/videos/static/videos")]
    files = []
    for f in files:
        l = f.split('.')
        extension = l[-1]
        base = '.'.join(l[:-1])
        v = Video(titre = base.replace('_', ' '), url=base,extension=extension)
        v.save()
