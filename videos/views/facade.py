from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.db.models import Count

from ..models import *

def can_proj(request):
    if request.user.is_authenticated:
        user = request.user
        return hasattr(user, 'utilisateur') and user.utilisateur.can_proj
    return False

def facade(request):
	if can_proj(request):
		return render(request,'facade.html')
	else:
		return HttpResponseRedirect(reverse('index'))

