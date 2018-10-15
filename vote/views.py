# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import get_object_or_404


def index(request):
    return HttpResponse("Working... for now")

import time, json, hashlib
#from urllib.urlparse import parse
#import urlurlparse.urlparse as parse
from urlparse import urlparse
import urllib

from rest_framework import viewsets, decorators
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny
from vote.models import *

#FKZ_KEY = b"WG7BF4pm"
FKZ_KEY = "WG7BF4pm"

def voter(request, student_id, video_id, category_id):
    student = get_object_or_404(Student, pk=student_id)
    video = get_object_or_404(VoteVideo, pk=video_id)
    c = get_object_or_404(VoteCategory, pk=category_id)
    v = Vote(student=student, category=c, video=video)
    v.save()
    return HttpResponseRedirect("http://binet-jtx.com/vaneau/#/vote/" + str(category_id))

def remove_vote(request, student_id, category_id):
    student = get_object_or_404(Student, pk=student_id)
    c = get_object_or_404(VoteCategory, pk=category_id)
    Vote.objects.filter(student=student,category=c).delete()
    return HttpResponseRedirect("http://binet-jtx.com/vaneau/#/vote/" + str(category_id))

class VoteCategoryViewSet(viewsets.ModelViewSet):
    queryset = VoteCategory.objects.all()
    serializer_class = VoteCategorySerializer

class VoteVideoViewSet(viewsets.ModelViewSet):
    queryset = VoteVideo.objects.all()
    serializer_class = VoteVideoSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @decorators.list_route(methods=['get'])
    def frankiz_auth_check(self, request):
        import logging
        logging.basicConfig(filename="/home/django/test.txt")
        logger = logging.getLogger(__name__)

        student = None
        response_data = {'valid': True, 'student': student}
        RETURN_PAGE = ('http://' + request.get_host() + '/vaneau/').encode()
        logger.error(RETURN_PAGE)

        if not "timestamp" in request.query_params.keys() or not "response" in request.query_params.keys() or not "hash" in request.query_params.keys():
            logger.error('KEYS')
            response_data["valid"] = False

        #response = urlparse.unquote_to_bytes(request.query_params.get("response"))
        response = urllib.unquote(request.query_params.get("response"))
        #ts = urlparse.unquote_to_bytes(request.query_params.get("timestamp"))
        ts = urllib.unquote(request.query_params.get("timestamp"))
        #h = urlparse.unquote_to_bytes(request.query_params.get("hash"))
        h = urllib.unquote(request.query_params.get("hash"))

        if abs(int(time.time()) - int(ts)) > 3600*3 or abs(int(ts) + 3*3600 - int(time.time())) < 30*60:
            logger.error('TS')
            response_data["valid"] = False

        if hashlib.md5(ts + FKZ_KEY + response).hexdigest() != h.decode():
            logger.error('HASH')
            response_data["valid"] = False

        if response_data["valid"]:
            data = json.loads(response.decode())
            try:
                student = Student.objects.get(hruid=data["hruid"])
            except Student.DoesNotExist:
                student = Student.objects.create(hruid=data["hruid"], lastname=data["lastname"], firstname=data["firstname"], promo=data["promo"])
            finally:
                response_data["student"] = StudentSerializer(student).data

        return Response(response_data, 200)

    @decorators.list_route(methods=['get'])
    def frankiz_url(self, request):
        ts = str(int(time.time())).encode()
        page = ('http://' + request.get_host() + '/vaneau/').encode()
        r = json.dumps(["names","promo"]).encode()
        h = hashlib.md5(ts + page + FKZ_KEY + r).hexdigest()
        return Response("http://www.frankiz.net/remote?" + urllib.unquote(urllib.urlencode([('timestamp',ts),('site',page),('hash',h),('request',r)])), 200)

# Function to verifiy if the requester has been authenticated by Frankiz
def frankiz_check(request):
    import logging
    logging.basicConfig(filename="/home/django/test.txt")
    logger = logging.getLogger(__name__)

    if not "timestamp" in request.query_params.keys() or not "response" in request.query_params.keys() or not "hash" in request.query_params.keys():
        logger.error('KEYS')
        raise NotAuthenticated()

    response = urllib.unquote(request.query_params.get("response"))
    ts = urllib.unquote(request.query_params.get("timestamp"))
    h = urllib.unquote(request.query_params.get("hash"))

    if abs(int(time.time()) - int(ts)) > 3600*3:
        logger.error('TS')
        raise NotAuthenticated()

    if hashlib.md5(ts + FKZ_KEY + response).hexdigest() != h.decode():
        logger.error('HASH')
        raise NotAuthenticated()

    data = json.loads(response.decode())

    return request

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (AllowAny, )
    filter_fields = ('category', 'student',)

    def retrieve(self, request, pk=None):
        #try:
        #    request = frankiz_check(request)
        #except NotAuthenticated:
        #    return Response("Not authenticated", 401)

        return super(VoteViewSet, self).retrieve(request, pk)

    def create(self, request):
        #try:
        #    request = frankiz_check(request)
        #except NotAuthenticated:
        #    return Response("Not authenticated", 401)

        return super(VoteViewSet, self).create(request)

    def update(self, request, pk=None):
        #try:
        #    request = frankiz_check(request)
        #except NotAuthenticated:
        #    return Response("Not authenticated", 401)

        return super(VoteViewSet, self).update(request, pk)

    def destroy(self, request, pk=None):
        #try:
        #    request = frankiz_check(request)
        #except NotAuthenticated:
        #    return Response("Not authenticated", 401)

        return super(VoteViewSet, self).destroy(request, pk)
