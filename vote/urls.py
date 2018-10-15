from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from vote.views import *

router = routers.DefaultRouter()
router.register(r'category', VoteCategoryViewSet)
router.register(r'video', VoteVideoViewSet)
router.register(r'student', StudentViewSet)
router.register(r'vote', VoteViewSet)

#urlpatterns = [
#    url(r'^', index),
#]
# router.register(r'user', UserViewSet)

urlpatterns = [
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^vote/voter/(?P<student_id>[0-9]+)/(?P<category_id>[0-9]+)/(?P<video_id>[0-9]+)$', voter, name='voter'),
    url(r'^vote/remove/(?P<student_id>[0-9]+)/(?P<category_id>[0-9]+)$', remove_vote, name='remove'),
    url(r'^', include(router.urls)),
]

