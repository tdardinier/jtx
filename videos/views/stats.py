#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Count
import datetime

from ..models import *
from .edit import *



def can_proj(request):
    if request.user.is_authenticated:
        user = request.user
        return hasattr(user, 'utilisateur') and user.utilisateur.can_proj
    return False

def transform_date(s):
	b = s.split(" ")
	b[0] = b[0].split("-")
	b[1] = b[1].split(":")
	return datetime.datetime(int(b[0][0]),int(b[0][1]),int(b[0][2]),int(b[1][0]),int(b[1][1]),int(float(b[1][2])))

def tri(s):
	return s[2]

def trih(s):
	return s[2].hour

def vues_par_jour(video_logs):
	video_logs.sort(key=tri)
	V = []
	D = []
	t = video_logs[0][2]
	d = 1
	for i in range(1,len(video_logs)):
		a = video_logs[i][2]
		if t.day == a.day and t.year == a.year and t.month == a.month:
			d += 1
		else:
			V.append(d)
			D.append(str(t.day) + "/" + str(t.month) + "/" + str(t.year))
			t = a
			d = 1
	if D[-1] != (str(t.day) + "/" + str(t.month) + "/" + str(t.year)):
		V.append(d)
		D.append(str(t.day) + "/" + str(t.month) + "/" + str(t.year))
	return [V,D]

def vues_par_heure(video_logs):
	video_logs.sort(key=trih)
	V2 = []
	D2 = []
	t = video_logs[0][2]
	d = 1
	for i in range(1,len(video_logs)):
		a = video_logs[i][2]
		if t.hour == a.hour:
			d += 1
		else:
			V2.append(d)
			D2.append(str(t.hour+1))
			t = a
			d = 1
	if D2[-1] != str(t.hour+1):
		V2.append(d)
		D2.append(str(t.hour+1))
	return [V2,D2]


def visiteurs_par_jour(video_logs):
	A = {}
	video_logs.sort(key=tri)
	V3 = []
	D3 = []
	t = video_logs[0][2]
	for i in range(1,len(video_logs)):
		a = video_logs[i][2]
		b = video_logs[i][0]
		if t.day == a.day and t.year == a.year and t.month == a.month:
			try:
				A[b] += 1
			except:
				A[b] = 1

		else:
			V3.append(len(A))
			D3.append(str(t.day) + "/" + str(t.month) + "/" + str(t.year))
			A = {}
			t = a

	if D3[-1] != (str(t.day) + "/" + str(t.month) + "/" + str(t.year)):
		V3.append(len(A))
		D3.append(str(t.day) + "/" + str(t.month) + "/" + str(t.year))

	return [V3,D3]

def video_plus_vues():
	a = Video.objects.all().order_by('-views')
	return a[:10]

def proj_plus_vues():
	a = Proj.objects.all().order_by('-views')
	return a[:10]

def utilisateurs_plus_actifs(video_logs):
	A = {}
	for i in video_logs:
		try:
			A[i[0]] += 1
		except:
			A[i[0]] = 1
	Truc = sorted(A.items(), key=lambda t: t[1], reverse=True)
	D4 = []
	for i in Truc:
		D4.append([get_object_or_404(User, pk=int(i[0])),i[1]])
	return D4[:10]


def stats(request):
	if can_proj(request):
		
		context={}

		#a = open("/home/django/jtx/video_logs.csv","r")
		a = open("C:/Users/Benoit/Documents/GitHub/jtx/video_logs.csv","r")
		videologs = a.read()
		a.close()
		videologs = videologs.split("\n")
		video_logs = [ videologs[i].split(";") for i in range(len(videologs)-1)]
		for i in range(len(video_logs)):
			video_logs[i][2] = transform_date(video_logs[i][2])
		context['vues_par_jour'] = vues_par_jour(video_logs)
		
		context['vues_par_heure'] = vues_par_heure(video_logs)

		context['visiteurs_par_jour'] = visiteurs_par_jour(video_logs)

		context['utilisateurs_plus_actifs'] = utilisateurs_plus_actifs(video_logs)

		context['proj_plus_vues'] = proj_plus_vues()

		context['video_plus_vues'] = video_plus_vues()

		context['max_nb_video'] = (context['video_plus_vues'])[0].views

		context['max_nb_proj'] = (context['proj_plus_vues'])[0].views

		context['max_nb_utilisateurs'] = (context['utilisateurs_plus_actifs'])[0][1]




		return render(request,'stats.html',context)
	
	else:
		return HttpResponseRedirect(reverse('index'))

def profil(request,user_id):
	if request.user.is_superuser:
		context = {}
		
		#a = open("/home/django/jtx/video_logs.csv","r")
		a = open("C:/Users/Benoit/Documents/GitHub/jtx/video_logs.csv","r")
		videologs = a.read()
		a.close()
		videologs = videologs.split("\n")
		video_logs = [ videologs[i].split(";") for i in range(len(videologs)-1)]
		A = []
		C = {}
		for i in range(len(video_logs)):
			video_logs[i][2] = transform_date(video_logs[i][2])
			if video_logs[i][0] == str(user_id):
				A.append(get_object_or_404(Video,pk=int(video_logs[i][1])))
				try:
					C[video_logs[i][1]] += 1
				except:
					C[video_logs[i][1]] = 1


		context['pourcentage_vu'] = str(len(C) / (Video.objects.all().count()) * 100)[:4]
		context['nb_videos_vues'] = len(C)
		context['historique'] = A[:10]
		B = sorted(C.items(),key=lambda x: x[1],reverse=True)
		D = []
		for i in B:
			D.append([get_object_or_404(Video,pk=int(i[0])),i[1]])
		print(D)
		context['videos_prefere'] = D[:5]
		context['nb_video_prefere'] = D[0][1]
		context['user'] = get_object_or_404(User,pk=user_id)

		return render(request,'profil.html',context)


	else:
		return HttpResponseRedirect(reverse('stats'))