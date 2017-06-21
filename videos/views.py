#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse

from .models import *

import random
from os import listdir

use_duration = False
n_page = 30
n_index = 5
n_suggestions = 5

if use_duration:
    from ffprobe import FFProbe

def filter(request, x):
    if not request.user.is_authenticated:
        x = x.filter(category__public=True)
    return x

def videos_request(request, q):
    l = q.split(" ")
    videos = filter(request, Video.objects)
    for x in l:
        videos = videos.filter(titre__contains = x)
    return videos.all()

def suggestions(request, q):
    videos = []
    if len(q) > 2:
        videos = videos_request(request, q)
    elements = [
        {
            'id': v.id,
            'titre': v.titre,
            'duree': v.duree,
        }
        for v in videos
    ]
    data = {
        'videos': elements,
    }
    return JsonResponse(data)

def search(request, page=1):
    q = request.GET.get('q', '')
    context = {
        'titre': u'Résultats de la recherche "' + q + '"',
        'elements': videos_request(request, q),
    }
    return render(request, 'videos.html', context)

def filter_tag(request, x):
    if not request.user.is_authenticated:
        x = x.filter(video__category__public=True)
    return x

def filter_category(request, x):
    if not request.user.is_authenticated:
        x = x.filter(public=True)
    return x

def can_proj(request):
    if request.user.is_authenticated:
        user = request.user
        return hasattr(user, 'utilisateur') and user.utilisateur.can_proj
    return False

def can_edit(request):
    if request.user.is_authenticated:
        user = request.user
        return hasattr(user, 'utilisateur') and user.utilisateur.can_edit
    return False

def id(x):
    return x

def real_add_proj(titre_proj, folder, c, promo):

    base_url = "http://binet-jtx.com/videos"
    base_folder = "/nfs/serveur/ftp"
    extensions_acceptees = ['mp4', 'avi']

    p = Proj(titre = titre_proj, category = c, promo = promo)
    p.save()
    files = [str(f) for f in listdir(str(base_folder + "/" + folder)) if str(f)[-3:] in extensions_acceptees]
    files.sort()
    i = 1
    for f in files:
        base = '.'.join(f.split('.')[:-1])
        filename = str(base_folder + "/" + folder + "/" + f)
        ld = []
        if use_duration:
            ld = FFProbe(filename).video
        d = 0
        if len(ld) > 0:
            dd = ld[0].duration
            d = int(float(dd if dd != "N/A" else "0"))
        titre = base.split('_')
        if titre[0][0] == '0':
            titre = titre[1:]
        v = Video(titre = ' '.join(titre), url = base_url + "/" + folder + "/" + f, duree=d, category=c)
        v.save()
        r = Relation_proj(proj = p, video = v, ordre = i)
        r.save()
        i += 1

def read_line_proj(line):
    l = line.split("@@")
    titre = l[0]
    folder = l[1] + "/MQ"
    c = Category.objects.get(titre=l[2])
    promo = int(l[3])
    real_add_proj(titre, folder, c, promo)

def auto_proj(l):
    for x in l:
        print("Reading " + x + "...")
        read_line_proj(x)
        print("Done")

def add_proj(request):

    context = {}
    version = "1.1"

    if can_proj(request):

        p = request.POST
        if 'folder' in p and 'titre' in p:

            #folder = "Evenements/Semaine_internationale/Houlgate_2017"
            #titre_proj = "Semaine internationale X2016 - Houlgate"

            folder = str(p['folder'])
            if folder[-1] == '/':
                folder = folder[:-1]
            folder = folder + "/MQ"
            titre_proj = p['titre']
            c = get_object_or_404(Category, pk=int(p['category']))

            real_add_proj(titre_proj, folder, c, int(p['promo']))
            context['message'] = u'Proj "' + titre_proj + u'" ajoutée avec succès !'

        else:
            context['message'] = "Version " + version
        context['categories'] = Category.objects.all()
    else:
        context['message'] = "Vous ne pouvez pas !"
    return render(request, 'add_proj.html', context)

def edit_video(request, video_id):

    context = {}

    if can_edit(request):

        v = get_object_or_404(Video, pk=video_id)
        p = request.POST

        if 'titre' in p:

            titre = str(p['titre'])
            url = str(p['url'])
            description = str(p['description'])
            duree = max(int(p['duree']), 0)
            c = get_object_or_404(Category, pk=int(p['category']))

            v.titre = titre
            v.url = url
            v.description = description
            v.duree = duree
            v.category = c
            v.save()

            return video(request, video_id)

        context['v'] = v
        context['categories'] = Category.objects.all()

    else:
        context['message'] = "Accès interdit !"

    return render(request, 'edit_video.html', context)

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
    c = Category.objects.get(titre="Proj JTX")
    v = filter(request, Proj.objects.filter(promo=year))
    context = {
        'year': year,
        'projs_jtx': v.filter(category=c),
        'projs_autres': v.exclude(category=c),
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
            'proj': proj,
            'suggestions': suggestions,
            'favorite': favorite,
            'epingle': epingle,
            'nb_jaimes': n,
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
    videos = filter_tag(request, tag.relation_tag_set)
    context = {
        'titre': tag.titre,
        'titre_tag': True,
        'id': tag_id,
    }
    return pagination(request, 'videos.html', context, videos, page, 'tag', lambda x: x.video)

def remove_favorite(request, video_id, home):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, pk=video_id)
        user = request.user
        c = Favorite.objects.filter(user = user, video = video).delete()
    if home == "1":
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('video', args=(video.id,)))

def remove_epingle(request, video_id, home):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, pk=video_id)
        user = request.user
        c = get_object_or_404(Favorite, user = user, video = video)
        c.epingle = False
        c.save()
    if home == "1":
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('video', args=(video.id,)))

def add_favorite(request, video_id):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, pk=video_id)
        user = request.user
        c = Favorite(user = user, video = video)
        c.save()
    return HttpResponseRedirect(reverse('video', args=(video.id,)))

def add_epingle(request, video_id):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, pk=video_id)
        user = request.user
        x = Favorite.objects.filter(user = user, video = video)
        if x.exists():
            c = x.all()[0]
            c.epingle = True
            c.save()
        else:
            c = Favorite(user = user, video = video, epingle = True)
            c.save()
    return HttpResponseRedirect(reverse('video', args=(video.id,)))

def remove_favorite_proj(request, proj_id, home):
    if request.user.is_authenticated:
        proj = get_object_or_404(Proj, pk=proj_id)
        user = request.user
        c = Favorite_proj.objects.filter(user = user, proj = proj).delete()
    if home == "1":
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('proj', args=(proj.id,)))

def remove_epingle_proj(request, proj_id, home):
    if request.user.is_authenticated:
        proj = get_object_or_404(Proj, pk=proj_id)
        user = request.user
        c = get_object_or_404(Favorite_proj, user = user, proj = proj)
        c.epingle = False
        c.save()
    if home == "1":
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('proj', args=(proj.id,)))

def add_favorite_proj(request, proj_id):
    if request.user.is_authenticated:
        proj = get_object_or_404(Proj, pk=proj_id)
        user = request.user
        c = Favorite_proj(user = user, proj = proj)
        c.save()
    return HttpResponseRedirect(reverse('proj', args=(proj.id,)))

def add_epingle_proj(request, proj_id):
    if request.user.is_authenticated:
        proj = get_object_or_404(Proj, pk=proj_id)
        user = request.user
        x = Favorite.objects.filter(user = user, proj = proj)
        if x.exists:
            c = x.all()[0]
            c.epingle = True
            c.save()
        else:
            c = Favorite_proj(user = user, proj = proj, epingle = True)
            c.save()
    return HttpResponseRedirect(reverse('proj', args=(proj.id,)))

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
