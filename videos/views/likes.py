#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse

from ..models import *

def remove_favorite(request, video_id, home):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, pk=video_id)
        user = request.user
        c = Favorite.objects.filter(user = user, video = video).delete()
        return HttpResponse("lannoo")
    return HttpResponse("holiner")
    """
    if home == "1":
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('video', args=(video.id,)))
    """

def remove_epingle(request, video_id, home):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, pk=video_id)
        user = request.user
        c = get_object_or_404(Favorite, user = user, video = video)
        c.epingle = False
        c.save()
        return HttpResponse("lannoo")
    return HttpResponse("holiner")
    """
    if home == "1":
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('video', args=(video.id,)))
    """

def add_favorite(request, video_id):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, pk=video_id)
        user = request.user
        c = Favorite(user = user, video = video)
        c.save()
        return HttpResponse("lannoo")
    return HttpResponse("holiner")
    """
    return HttpResponseRedirect(reverse('video', args=(video.id,)))
    """

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
        return HttpResponse("lannoo")
    return HttpResponse("holiner")
    """
    return HttpResponseRedirect(reverse('video', args=(video.id,)))
    """

def remove_favorite_proj(request, proj_id, home):
    if request.user.is_authenticated:
        proj = get_object_or_404(Proj, pk=proj_id)
        user = request.user
        c = Favorite_proj.objects.filter(user = user, proj = proj).delete()
        return HttpResponse("lannoo")
    return HttpResponse("holiner")
    """
    if home == "1":
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('proj', args=(proj.id,)))
    """

def remove_epingle_proj(request, proj_id, home):
    if request.user.is_authenticated:
        proj = get_object_or_404(Proj, pk=proj_id)
        user = request.user
        c = get_object_or_404(Favorite_proj, user = user, proj = proj)
        c.epingle = False
        c.save()
        return HttpResponse("lannoo")
    return HttpResponse("holiner")
    """
    if home == "1":
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('proj', args=(proj.id,)))
    """

def add_favorite_proj(request, proj_id):
    if request.user.is_authenticated:
        proj = get_object_or_404(Proj, pk=proj_id)
        user = request.user
        c = Favorite_proj(user = user, proj = proj)
        c.save()
        return HttpResponse("lannoo")
    return HttpResponse("holiner")
    """
    return HttpResponseRedirect(reverse('proj', args=(proj.id,)))
    """

def add_epingle_proj(request, proj_id):
    if request.user.is_authenticated:
        proj = get_object_or_404(Proj, pk=proj_id)
        user = request.user
        x = Favorite_proj.objects.filter(user = user, proj = proj)
        if x.exists():
            c = x.all()[0]
            c.epingle = True
            c.save()
        else:
            c = Favorite_proj(user = user, proj = proj, epingle = True)
            c.save()
        return HttpResponse("lannoo")
    return HttpResponse("holiner")
"""
    return HttpResponseRedirect(reverse('proj', args=(proj.id,)))
"""

def unlike_comment(request, comment_id):
    if request.user.is_authenticated:
        c = get_object_or_404(Relation_comment, pk=comment_id)
        user = request.user
        r = Like_comment.objects.filter(user = user, comment = c).delete()
        return HttpResponse(str(comment_id))
    return HttpResponse("erreur")

def like_comment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Relation_comment, pk=comment_id)
        user = request.user
        r = Like_comment(user = user, comment = comment)
        r.save()
        return HttpResponse(str(comment_id))
    return HttpResponse("erreur")
    
def like_comment_proj(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Relation_comment_proj, pk=comment_id)
        user = request.user
        r = Like_comment_proj(user = user, comment = comment)
        r.save()
        return HttpResponse(str(comment_id))
    return HttpResponse("erreur")
    


def unlike_comment_proj(request, comment_id):
    if request.user.is_authenticated:
        c = get_object_or_404(Relation_comment_proj, pk=comment_id)
        user = request.user
        r = Like_comment_proj.objects.filter(user = user, comment = c).delete()
        return HttpResponse(str(comment_id))
    return HttpResponse("erreur")
   