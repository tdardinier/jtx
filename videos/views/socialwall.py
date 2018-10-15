from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from ..models import *


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


def messageurgent(request):
	if can_proj(request):
		context = {}
		if "message" in request.POST:
			a = request.POST["message"]
			p = Messagelive(message=a,aprrouve=True,deja_envoye=False,prio=True)
			p.save();
			context["messagerecu"] = True
		
		return render(request,"messageurgent.html",context)
	else:
		return HttpResponseRedirect(reverse("index"))


def socialwall(request):

	post = request.POST

	context={}

	if "message" in post:
		a = Messagelive(message = post["message"],aprrouve=False,deja_envoye=False)
		a.save()

		context["messagerecu"] = True

	return render(request,"add_message_socialwall.html",context)

def jssocialwall(request):
	if can_proj(request):

		a = Messagelive.objects.filter(aprrouve=True,deja_envoye=False,prio=True)
		if a.exists():
			i = a[0]
			i.deja_envoye=True
			reponse = {"statut":"bon","message":i.message}
			i.delete()
			return JsonResponse(reponse)

		a = Messagelive.objects.filter(aprrouve=True,deja_envoye=False)
		if a.exists():
			i = a[0]
			i.deja_envoye=True
			i.save()
			reponse = {"statut":"bon","message":i.message}
			return JsonResponse(reponse)
		else:
			a = Messagelive.objects.filter(aprrouve=True)
			if a.exists():
				i = a.order_by('?')[0]
				reponse = {"statut":"bon","message":i.message}
				return JsonResponse(reponse)
			else:
				return JsonResponse({'statut':"pas bon"})
	else:
		return JsonResponse({'statut':"pas bon"})

def adminsocialwall(request):
	if can_proj(request):
		messages = Messagelive.objects.filter(aprrouve=False)
		context = {"messages":messages}
		return render(request,"admin_socialwall.html",context)
	else:
		return HttpResponseRedirect(reverse("index"))

def jsadminsocialwall(request):
	if can_proj(request):
		if "id" in request.POST and "statut" in request.POST:
			a = get_object_or_404(Messagelive,pk=int(request.POST["id"]))
			if request.POST["statut"] == "valide":
				a.aprrouve=True
				a.save()
			else:
				a.delete()
		return JsonResponse({"statut":"bon"})
	else:
		return JsonResponse({"statut":"pas bon"})

def printsocialwall(request):
	if can_proj(request):
		return render(request,"socialwall.html",{})
	else:
		return HttpResponseRedirect(reverse("index"))