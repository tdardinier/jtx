#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Count
from time import sleep

from ..models import *

def can_proj(request):
    if request.user.is_authenticated:
        user = request.user
        return hasattr(user, 'utilisateur') and user.utilisateur.can_proj
    return False

def facade(request):
	if can_proj(request):
		#a = open("facade.txt",'w')
		#a.write(u"Trailers;Rétros;éèàùêûîôû%§;9988;9988;9988;9988;9988;9988;9988;9988;9988;9988;9988")
		#a.close()
		a = open("/home/django/jtx/facade.txt","r")
		videos = a.read().decode('utf-8').split(u";")
			
		context={'background': videos[3],
					 'presta':videos[4],
						}
		a.close()
		for i in range(2,len(videos)):
			context["vid_"+str(i-2)] = videos[i]

		for i in context:
			try:
				t = int(context[i])
				context[i] = get_object_or_404(Video,pk=int(context[i]))
			except:
				t = 64
		context['nom_cat1'] = videos[0]
		context['nom_cat2'] = videos[1]
		context['nom_cat3'] = videos[2]
		context['can_proj'] = can_proj(request)
		return render(request,'facade.html',context)
	else:
		return HttpResponseRedirect(reverse('index'))

def modifier_facade(request):
	if can_proj(request):
		post = request.POST
		if 'vid_background' in post:
			a = open("/home/django/jtx/facade.txt","w")
			fichier = post["nom_cat1"] + ";" + post["nom_cat2"] + ";" + post["nom_cat3"]

			for i in post:
				if i[:3] == "vid":
					fichier = fichier + ";" + post[i]
			a.write(fichier)
			a.close()
			return HttpResponseRedirect(reverse('facade'))

		else:
			a = open("/home/django/jtx/facade.txt","r")
			videos = a.read()decode('utf-8').split(";")
			
			context={'background': videos[3],
					 'presta':videos[4],
					 'nom_cat1':videos[0],
					 'nom_cat2':videos[1],
					 'nom_cat3':videos[2],
						}
			a.close()
			for i in range(2,len(videos)):
				context["vid_"+str(i-2)] = videos[i]

			return render(request,'modifier_facade.html',context)

	else:
		HttpResponseRedirect(reverse('facade'))


