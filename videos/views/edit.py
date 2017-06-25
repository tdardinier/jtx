#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse

from ..models import *

from os import listdir

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

def edit_proj(request, proj_id):

    context = {}

    if can_proj(request):

        p = get_object_or_404(Proj, pk=proj_id)
        post = request.POST

        if 'titre' in post:

            titre = post['titre']
            c = get_object_or_404(Category, pk=int(post['category']))
            promo = max(int(post['promo']), 0)
            image = post['image']

            p.titre = titre
            p.image = image
            p.promo = promo
            p.category = c

            p.save()

            for x in post:
                if x[:8] == "r_video_":
                    y = int(x[8:])
                    r = Relation_proj.objects.get(pk=y)
                    r.ordre = int(post[x])
                    r.save()


            return HttpResponseRedirect(reverse('proj', args=(p.id,)))

        context['p'] = p
        context['categories'] = Category.objects.all()

    else:
        context['message'] = "Accès interdit !"

    return render(request, 'edit_proj.html', context)

def edit_video(request, video_id):

    context = {}

    if can_edit(request):

        v = get_object_or_404(Video, pk=video_id)
        p = request.POST

        if 'titre' in p:

            titre = p['titre']
            url = p['url']
            description = p['description']
            duree = max(int(p['duree']), 0)
            c = get_object_or_404(Category, pk=int(p['category']))

            v.titre = titre
            v.url = url
            v.description = description
            v.duree = duree
            v.category = c
            v.save()

            # TAGS



            for x in post:
                if x[:8] == "r_video_":
                    y = int(x[8:])
                    r = Relation_proj.objects.get(pk=y)
                    r.ordre = int(post[x])
                    r.save()



            return HttpResponseRedirect(reverse('video', args=(v.id,)))

        context['v'] = v
        context['categories'] = Category.objects.all()
        context['auteurs'] = Auteur.objects.all()
        context['tags'] = Tag.objects.all()

    else:
        context['message'] = "Accès interdit !"

    return render(request, 'edit_video.html', context)


