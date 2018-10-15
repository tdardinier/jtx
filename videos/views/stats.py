#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import connection as conection
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Count
import datetime
import time


from ..models import *
from .edit import *


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
	return a[:100]

def proj_plus_vues():
	a = Proj.objects.all().order_by('-views')
	return a[:100]

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
		if User.objects.filter(pk=int(i[0])).exists():
			D4.append([get_object_or_404(User, pk=int(i[0])),i[1]])
	return D4[:100]


def stats(request):
	if can_proj(request):

		video = video_plus_vues()[0]
		n = Favorite.objects.filter(video = video).count()
		user = request.user
		favorite = Favorite.objects.filter(user = user, video = video).exists()
		epingle = Favorite.objects.filter(user = user, video = video, epingle = True).exists()
		context = {
			'can_edit': can_edit(request),
			'can_proj' : can_proj(request),
			'video': video,
			'favorite': favorite,
			'epingle': epingle,
			'nb_jaimes': n,
			}

		t1 = time.time()
		videologs = Videovue.objects.all()
		print(time.time()-t1)
		video_logs = []

		cursor = conection.cursor()
		cursor.execute("SELECT user_id,video_id,date FROM videos_videovue")
		row = cursor.fetchall()

		video_logs=[list(r) for r in row]		

		#video_logs = [ [vid.user.id,vid.video.id,vid.date] for vid in videologs]


		print(time.time()-t1)
		context['vues_par_jour'] = vues_par_jour(video_logs)
		print(time.time()-t1)
		context['vues_par_heure'] = vues_par_heure(video_logs)
		print(time.time()-t1)
		context['visiteurs_par_jour'] = visiteurs_par_jour(video_logs)
		print(time.time()-t1)
		context['utilisateurs_plus_actifs'] = utilisateurs_plus_actifs(video_logs)
		print(time.time()-t1)
		context['proj_plus_vues'] = proj_plus_vues()
		print(time.time()-t1)
		context['video_plus_vues'] = video_plus_vues()
		print(time.time()-t1)
		context['max_nb_video'] = (context['video_plus_vues'])[0].views
		print(time.time()-t1)
		context['max_nb_proj'] = (context['proj_plus_vues'])[0].views
		print(time.time()-t1)
		context['max_nb_utilisateurs'] = (context['utilisateurs_plus_actifs'])[0][1]
		print(time.time()-t1)



		return render(request,'stats.html',context)
	
	else:
		return HttpResponseRedirect(reverse('index'))

def profil(request,user_id):
	if int(request.user.id) == int(user_id) or request.user.is_superuser:
		context = {}
		
		#a = open("/home/django/jtx/video_logs.csv","r")
		#a = open("C:/Users/Benoit/Documents/GitHub/jtx/video_logs.csv","r")
		#videologs = a.read()
		#a.close()
		user = get_object_or_404(User,pk=user_id)
		videovues = Videovue.objects.filter(user=user).order_by("-date")

		Q = set()
		for i in videovues:
			Q.add(i.video)
		C = []
		for vid in Q:
			C.append([vid,Videovue.objects.filter(video=vid,user=user).count()])


		context['pourcentage_vu'] = str(float(len(C)) / (Video.objects.all().count()) *100)[:5]
		context['nb_videos_vues'] = len(C)
		context['historique'] = [[a.video,a.date] for a in videovues[:100]]

		B = sorted(C,key=lambda x: x[1],reverse=True)
		context['videos_prefere'] = B[:20]
		context['nb_video_prefere'] = B[0][1]
		context['user'] = get_object_or_404(User,pk=user_id)

		return render(request,'profil.html',context)


	else:
		return HttpResponseRedirect(reverse('stats'))


def pas_un_fdp2(user,video,date):
	videos_vues = Videovue.objects.filter(user=user,video=video,date__gt=date-datetime.timedelta(days=1))
	if len(videos_vues) > 5:
		return False
	else:
		return True

#def traiter_videos_vues(request):
#	Videovue.objects.all().delete()
#	a = open("video_logs.csv","r")
#	logs = a.read().split("\n")
#	A = 0
#	B = len(logs)
#	for l in logs:
#		try:
#			log = l.split(";")
#			if log[0] != "0":
#				if User.objects.filter(pk=int(log[0])).exists() and Video.objects.filter(pk=int(log[1])).exists():
#					user = get_object_or_404(User,pk=int(log[0]))
#					video = get_object_or_404(Video,pk=int(log[1]))
#					if pas_un_fdp2(user,video,transform_date(log[2])):
#						v = Videovue(user=user,video=video,date=transform_date(log[2]),credibilite=1)
#						v.save()
#					else:
#						video.views -= 1
#						video.save()
#		except ValueError:
#			(print("fini"))
#		A += 1
#		if A%(B//100) == 0:
#			print("Traitement fini à " + str(int(A/B*100+0.5)) + " % ")
#
#	return HttpResponse("c'est bon")

