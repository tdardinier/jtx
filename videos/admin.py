from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.apps import apps

app = apps.get_app_config('videos')

for model_name, model in app.models.items():
    admin.site.register(model)

class FavoriteInline(admin.TabularInline):
    model = Favorite
    user = User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [FavoriteInline]

class CommentProjAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'proj', 'date']
    list_filter = ['proj', 'date']
    search_fields = ['comment', 'proj__titre']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'video', 'date']
    list_filter = ['video', 'date']
    search_fields = ['comment', 'video__titre']

admin.site.unregister(Relation_comment)
admin.site.register(Relation_comment, CommentAdmin)

admin.site.unregister(Relation_comment_proj)
admin.site.register(Relation_comment_proj, CommentProjAdmin)

# --------------------
# --------------------
# Video
# --------------------
# --------------------

class TagInline(admin.TabularInline):
    model = Relation_tag
    extra = 0

class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'titre', 'date', 'views', 'category']
    list_filter = ['date', 'views', 'category']
    search_fields = ['titre']
    inlines = [TagInline]

admin.site.unregister(Video)
admin.site.register(Video, VideoAdmin)

# --------------------
# --------------------
# Proj
# --------------------
# --------------------

class VideoInline(admin.TabularInline):
    model = Relation_proj
    extra = 0

class ProjAdmin(admin.ModelAdmin):
    list_display = ['id', 'titre', 'category', 'date', 'views']
    list_filter = ['category', 'date', 'views']
    search_fields = ['titre', 'category__titre']
    inlines = [VideoInline]

admin.site.unregister(Proj)
admin.site.register(Proj, ProjAdmin)

# --------------------
# --------------------
# Category
# --------------------
# --------------------

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'titre', 'public']
    list_filter = ['public']
    search_fields = ['titre']

admin.site.unregister(Category)
admin.site.register(Category, CategoryAdmin)
