#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Count
from time import sleep
from django.core.mail import send_mail

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
		#a = open("facade.txt","r")
		#videos = a.read().split(";")
		a = open("/home/django/jtx/facade.txt","r")
		videos = a.read().decode('utf-8').split(u";")
			
		context={'background': videos[3],
					 'presta':videos[4],
						}
		a.close()
		for i in range(5,len(videos)):
			context["vid_"+str(i-4)] = videos[i]

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
			fichier = post["nom_cat1"] + ";" + post["nom_cat2"] + ";" + post["nom_cat3"] + ";" + post["vid_background"] + ";" + post["vid_presta"] + ";" + post["vid_1"] + ";" + post["vid_2"] + ";" + post["vid_3"] + ";" + post["vid_4"] + ";" + post["vid_5"] + ";" + post["vid_6"] + ";" + post["vid_7"] + ";" + post["vid_8"] + ";" + post["vid_9"]
			a.write(fichier.encode('utf-8'))
			a.close()
			return HttpResponseRedirect(reverse('facade'))

		else:
			a = open("/home/django/jtx/facade.txt","r")
			videos = a.read().decode('utf-8').split(";")
			
			context={'background': videos[3],
					 'presta':videos[4],
					 'nom_cat1':videos[0],
					 'nom_cat2':videos[1],
					 'nom_cat3':videos[2],
						}
			a.close()
			for i in range(5,len(videos)):
				context["vid_"+str(i-4)] = videos[i]

			return render(request,'modifier_facade.html',context)

	else:
		HttpResponseRedirect(reverse('facade'))

def treat_facade(request):
	post = request.POST
	name = post["name"]
	email = post["email"]
	message = post["message"]

	a = open("/home/django/jtx/messages_facade.csv","a")
	#a = open("message_facade.csv","a")
	tout = "\n ------ \n" + "Nom de l'expéditeur : " + name + "\n Son adresse email : " + email + " \n Son message : " + message
	a.write(tout.encode('utf-8'))
	a.close()


	return HttpResponse(u"Message bien reçu, merci")

def messages_facade(request):
	if can_proj(request):

		a = open("/home/django/jtx/messages_facade.csv","r")
		texte = a.read().decode("utf-8").split(u"\n ------ \n")
		messages = []
		for i in range(1,len(texte)):
			messages.append(texte[len(texte)-i].replace("\n","</p>"))

		return render(request,'messages_facade.html',{"messages":messages})

	else:
		return HttpResponseRedirect(reverse('index'))
