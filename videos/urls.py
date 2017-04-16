from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.populate_bdd, name='test'),
    url(r'^login/$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': views.index}, name='logout'),
    url(r'^projs/(?P<page>[0-9]+)/$', views.projs, name='projs'),
    url(r'^proj/(?P<proj_id>[0-9]+)/$', views.proj, name='proj'),
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^category/(?P<category_id>[0-9]+)/(?P<page>[0-9]+)/$', views.category, name='category'),
    url(r'^videos/(?P<page>[0-9]+)/$', views.videos, name='videos'),
    url(r'^video/(?P<video_id>[0-9]+)/$', views.video, name='video'),
    url(r'^favorites/(?P<page>[0-9]+)/$', views.favorites, name='favorites'),
    url(r'^tags/$', views.tags, name='tags'),
    url(r'^tag/(?P<tag_id>[0-9]+)/(?P<page>[0-9]+)/$', views.tag, name='tag'),
    url(r'^add_favorite/(?P<video_id>[0-9]+)/$', views.add_favorite, name='add_favorite'),
    url(r'^remove_favorite/(?P<video_id>[0-9]+)/$', views.remove_favorite, name='remove_favorite'),
    url(r'^comment_video/(?P<video_id>[0-9]+)/$', views.comment_video, name='comment_video'),
    url(r'^comment_proj/(?P<proj_id>[0-9]+)/$', views.comment_proj, name='comment_proj'),
]
