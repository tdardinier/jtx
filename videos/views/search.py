#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse

from django.db.models import Q

from ..models import *

def search(request, page=1):
    q = request.GET.get('q', '')
    context = {
        'titre_search': True,
        'titre': u'Résultats de la recherche "' + q + '"',
        'elements_vid': videos_request(request, q),
        'elements_proj': proj_request(request, q),
    }
    return render(request, 'search.html', context)

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

def proj_request(request, q):
    l = q.split(" ")
    projs = filter(request, Proj.objects)
    for x in l:
        projs = projs.filter(titre__contains = x)
    return projs.all()

def auteurs_request(request, q):
    l = q.split(" ")
    auteurs = Auteur.objects
    for x in l:
        auteurs = auteurs.filter(Q(firstname__contains = x) | Q(lastname__contains = x))
    return auteurs.all()

def suggestions(request, q):
    videos = []
    projs = []
    auteurs = []
    if len(q) >= 2:
        videos = videos_request(request, q)
        projs = proj_request(request, q)
        auteurs = auteurs_request(request, q)
    elements_video = [
        {
            'url': reverse('video', args=(v.id,)),
            'titre': v.titre,
            'duree': v.duree,
        }
        for v in videos]
    elements_proj = [
        {
            'url': reverse('proj', args=(p.id,)),
            'titre': p.titre,
        }
        for p in projs]
    elements_auteur = [
        {
            'url': reverse('jtxman', args=(a.id,1,)),
            'promo': a.promo,
            'firstname': a.firstname,
            'lastname': a.lastname,
        }
        for a in auteurs]
    data = {
        'videos': elements_video[:10],
        'projs': elements_proj[:10],
        'auteurs': elements_auteur[:10],
    }
    return JsonResponse(data)

def filter_relation(request, x):
    if not request.user.is_authenticated:
        x = x.filter(video__category__public=True)
    return x

def filter_category(request, x):
    if not request.user.is_authenticated:
        x = x.filter(public=True)
    return x
