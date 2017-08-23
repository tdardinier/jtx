#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from ..models import Utilisateur

def connection(request):

    # TODO: securiser tout

    PHPSESSID = request.GET.get('PHPSESSID', '')
    auth = request.GET.get('auth', '')
    forlife = request.GET.get('forlife', '')
    prenom = request.GET.get('prenom', '')
    nom = request.GET.get('nom', '')
    promo = request.GET.get('promo', '')

    pw = "automatic"

    user = authenticate(username = forlife, password = pw)

    if user is not None:
        login(request, user)
    else:
        user = User.objects.create_user(username=forlife, password=pw)
        Utilisateur.objects.create(user=user)
        login(request, user)

    return redirect('index')
