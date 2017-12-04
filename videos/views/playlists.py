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
            if a.filter(video_suivante=video).exists() or a.filter(video_precedente=video).exists() or (last_video != None and last_video == video):
                context['message'] = u'Désolé mais la vidéo est déjà dans cette playlist'
            else:
                if last_video == None:
                    titre_playlist.last_video = video
                    titre_playlist.save()
                else:
                    real_add_playlist(titre_playlist, last_video, video)
                    titre_playlist.last_video = video
                    titre_playlist.save()

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
        context["titre_playlist"] = titre_playlist
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

def tri(A):
    return A[1]

def edit_playlist(request, playlist_id):

    context = {}

    if can_proj(request):

        p = get_object_or_404(Titreplaylist, pk=playlist_id)
        post = request.POST

        if 'titre' in post:

            titre = post['titre']
            p.label = titre

            p.save()
            videos = []

            for x in post:
                if x[:11] == "r_playlist_":
                    y = int(x[11:])
                    ordre = int(post[x])
                    if post['v_playlist_' + str(y)] == 'Y':
                        videos.append([get_object_or_404(Playlist,pk=y).video_precedente, ordre])
                    a = get_object_or_404(Playlist, pk=y)
                    a.delete()
                if x == 'last_video':
                    ordre = int(post[x])
                    if post['vlastvideo'] == 'Y':
                        videos.append([p.last_video,ordre])


            videos.sort(key=tri)
            try:
                for i in range(len(videos)-1):
                    if i >= 0:
                        r = Playlist(titre_playlist=p,video_precedente=videos[i][0],video_suivante=videos[i+1][0])
                        r.save()
                        p.last_video = videos[len(videos)-1][0]
                        p.save()
            except:
                try:
                    p.last_video = videos[0][0]
                    p.save()
                except:
                    p.last_video = None
                    p.save() 



            return HttpResponseRedirect(reverse('visualiser_playlist', args=(p.id,)))

        context['p'] = p
        context['playlists'] = Playlist.objects.filter(titre_playlist=p)
        context['last_video'] = p.last_video
        context['nbr'] = len(context['playlists']) + 1
        return render(request, 'edit_playlist.html', context)

    else:
        return HttpResponseRedirect(reverse('index'))



