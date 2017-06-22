from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test/$', views.add_proj, name='add_proj'),
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
    url(r'^jtxman/(?P<auteur_id>[0-9]+)/(?P<page>[0-9]+)/$', views.jtxman, name='jtxman'),

    url(r'^add_favorite/(?P<video_id>[0-9]+)/$', views.add_favorite, name='add_favorite'),
    url(r'^add_favorite_proj/(?P<proj_id>[0-9]+)/$', views.add_favorite_proj, name='add_favorite_proj'),
    url(r'^remove_favorite/(?P<video_id>[0-9]+)/(?P<home>[0-1])/$', views.remove_favorite, name='remove_favorite'),
    url(r'^remove_favorite_proj/(?P<proj_id>[0-9]+)/(?P<home>[0-1])/$', views.remove_favorite_proj, name='remove_favorite_proj'),

    url(r'^add_epingle/(?P<video_id>[0-9]+)/$', views.add_epingle, name='add_epingle'),
    url(r'^add_epingle_proj/(?P<proj_id>[0-9]+)/$', views.add_epingle_proj, name='add_epingle_proj'),
    url(r'^remove_epingle/(?P<video_id>[0-9]+)/(?P<home>[0-1])/$', views.remove_epingle, name='remove_epingle'),
    url(r'^remove_epingle_proj/(?P<proj_id>[0-9]+)/(?P<home>[0-1])/$', views.remove_epingle_proj, name='remove_epingle_proj'),

    url(r'^comment_video/(?P<video_id>[0-9]+)/$', views.comment_video, name='comment_video'),
    url(r'^comment_proj/(?P<proj_id>[0-9]+)/$', views.comment_proj, name='comment_proj'),
    url(r'^edit_video/(?P<video_id>[0-9]+)/$', views.edit_video, name='edit_video'),
    url(r'^jtx/(?P<year>[0-9]+)/$', views.jtx, name='jtx'),
    url(r'^search/$', views.search, name='search'),
    url(r'^suggestions/(?P<q>[\w|\W]*)/$', views.suggestions, name='suggestions'),
]
