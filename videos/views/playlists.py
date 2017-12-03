#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from ..models import *
from .edit import *



def can_proj(request):
    if request.user.is_authenticated:
        user = request.user
        return hasattr(user, 'utilisateur') and user.utilisateur.can_proj
    return False


def create_playlist(request):

    context = {}
    version = "1.1"

    if can_proj(request):

        p = request.POST
        if 'titre_playlist' in p:



            a = Titreplaylist.objects.filter(label=p['titre_playlist']).exists()

            if a:
                context['message'] = u'Désolé mon lieutenant, la playlist ' + p['titre_playlist'] + u' existe déjà'

            else:
                b = Titreplaylist(label=p['titre_playlist'])
                b.save()
                context['message'] = u'Playlist "' + p['titre_playlist'] + u'" ajoutée avec succès !'

        else:
            context['message'] = "Version " + version

    else:
        context['message'] = "Vous ne pouvez pas !"
    return render(request, 'create_playlist.html', context)




def real_add_playlist(titre_playlist, video_precedente, video_suivante):

    
    p = Playlist(titre_playlist = titre_playlist, video_precedente = video_precedente, video_suivante=video_suivante)
    p.save()

def add_playlist(request, video_id):

    context = {}
    version = "1.1"

    if can_proj(request):

        p = request.POST
        if 'video' in p and 'titres_playlists' in p:

            
            titre_playlist = get_object_or_404(Titreplaylist, pk=int(p['titres_playlists']))
            video = get_object_or_404(Video, pk=int(p['video']))

            a = Playlist.objects.filter(titre_playlist=titre_playlist)
            last_video = titre_playlist.last_video
            if a.filter(video_suivante=video).exists() or (last_video != None and last_video.pk == video.pk):
                context['message'] = u'Désolé mais la vidéo est déjà dans cette playlist'
            else:
                if last_video == None:
                    titre_playlist.last_video = video
                    titre_playlist.save()
                else:
                    real_add_playlist(titre_playlist, last_video, video)
                    titre_playlist.last_video = video
                    titre_playlist.save()
                context['message'] = u'PLaylist "' + titre_playlist.label + u'" ajoutée avec succès !'
                context['video_id'] = video_id
                return HttpResponseRedirect(reverse('video', args=(video_id,)))
 

        else:
            context['message'] = "Version " + version
            
        context['video_id'] = video_id
        context['titres_playlists'] = Titreplaylist.objects.all()
        return render(request, 'add_playlist.html', context)
    else:
        context['message'] = "Vous ne pouvez pas !"
    return HttpResponseRedirect(reverse('video', args=(video_id,)))

def visualiser_playlist(request, playlist_id):
    if request.user.is_authenticated:
        titre_playlist = get_object_or_404(Titreplaylist, pk=playlist_id)
        playlists = Playlist.objects.filter(titre_playlist=titre_playlist)
        context = {}
        context["titre_playlist"] = titre_playlist.label
        context['playlists'] = playlists
        context['last_video'] = titre_playlist.last_video
        context['can_proj'] = can_proj(request)
        return render(request, 'playlist.html', context)

    else:
        return HttpResponseRedirect(reverse('index'))

def playlists(request):
    if request.user.is_authenticated:
        titres_playlists= Titreplaylist.objects.all()
        context = {}
        context['playlists'] = titres_playlists
        return render(request, 'playlists.html', context)

    else:
        return HttpResponseRedirect(reverse('index'))


