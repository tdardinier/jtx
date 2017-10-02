#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess as sp
import json
import os

def probe(vid_file_path):
    ''' Give a json from ffprobe command line

    @vid_file_path : The absolute (full) path of the video file, string.
    '''
    if type(vid_file_path) != str:
        # raise Exception('Give ffprobe a full file path of the video')
        return 1.

    command = ["ffprobe",
            "-loglevel",  "quiet",
            "-print_format", "json",
             "-show_format",
             "-show_streams",
             vid_file_path
             ]

    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()
    return json.loads(out)

def duration(vid_file_path):
    ''' Video's duration in seconds, return a float number
    '''
    _json = probe(vid_file_path)

    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])

    if 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])

    # if everything didn't happen,
    # we got here because no single 'return' in the above happen.
    # raise Exception('I found no duration')
    return 1.
    #return None

from django.shortcuts import render, get_object_or_404

from ..models import *
from .edit import *

def real_add_proj(titre_proj, folder, c, promo):

    base_url = "/videos"
    base_folder = "/nfs/serveur/ftp"
    extensions_acceptees = ['mp4', 'avi']

    p = Proj(titre = titre_proj, category = c, promo = promo)
    p.save()
    base_basique = str(base_folder + "/" + folder + "/")

    quality = "HD"
    if not os.path.exists(base_basique + quality):
        quality = "MD"
    if not os.path.exists(base_basique + quality):
        quality = "LQ"

    files = [str(f) for f in listdir(base_basique + quality) if str(f)[-3:] in extensions_acceptees]
    files.sort()

    i = 1
    for f in files:

        basename = '.'.join(f.split('.')[:-1])
        filename = str(base_folder + "/" + folder + "/HD/" + f)
        d = duration(filename)
        titre = basename.split('_')

        base_liens = base_url + "/" + folder + "/"
        hd = base_liens + "HD/" + f
        md = base_liens + "MD/" + f
        sd = base_liens + "LQ/" + f
        if quality == "MD":
            hd = ""
        if quality == "LQ":
            hd = ""
            md = ""
        sub = base_liens + "sub/" + basename + ".srt.vtt"
        if not os.path.exists(base_folder + "/" + folder + "/sub/" + basename + ".srt.vtt"):
            sub = ""
        snap = base_liens + "snaps/" + f + ".png"

        if titre[0][0] in ['0', '1']:
            titre = titre[1:]
        v = Video(titre = ' '.join(titre), duree=d, category=c, hd=hd, md=md, sd=sd, screenshot=snap, subtitles=sub)
        v.save()
        r = Relation_proj(proj = p, video = v, ordre = i)
        r.save()
        i += 1

def read_line_proj(line):
    l = line.split("@@")
    titre = l[0]
    folder = l[1]
    c = Category.objects.get(titre="Divers")
    a = Category.objects.filter(titre=l[2])
    if a.exists():
        c = a.first()
    promo = int(l[3])
    real_add_proj(titre, folder, c, promo)

def auto_proj(l):
    for x in l:
        if x != "\n" and x[0] != "#":
            print("Reading " + x + "...")
            read_line_proj(x)
            print("Done")
        elif x != "\n":
            print("Ignoring " + x[:-2])

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
