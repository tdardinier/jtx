#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from ..models import *

use_duration = False

if use_duration:
    from ffprobe import FFProbe

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
        if titre[0][0] in ['0', '1']:
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

 
