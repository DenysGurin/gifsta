import redis

from django.contrib import admin
from django.core.cache import cache

from .models import Gif, Like, Hashtag, GifHashtagLinker, GifView, Category


def update_cache():
    try:
        cache.set('to_update', True)
    except redis.exceptions.ConnectionError:
        pass

def make_published(modeladmin, request, queryset):
    queryset.update(post_to=True)
    update_cache()
make_published.short_description = "Selected gifs as published"

def make_hide(modeladmin, request, queryset):
    queryset.update(post_to=False)
    update_cache()
make_hide.short_description = "Selected gifs as hided"

class TermInlineGif(admin.TabularInline):
    model = Like#.terms.through
    fk_name = "gif_id"
class TermInlineHashtag(admin.TabularInline):
    model = GifHashtagLinker#.terms.through
    
class GifAdmin(admin.ModelAdmin):
    inlines = (TermInlineGif, TermInlineHashtag)
    actions = [make_published, make_hide]
    list_display = ('id', 'creator', 'name', 'tags', 'post_to', 'upload_date')
    # fields = "__all__"
    class Meta:
        model = Gif
        fields = '__all__'

    # fields = ('creator', 'name', 'tags', 'post_to', 'shocked', 'loved', 'laugh', 'gif_file', 'prev_gif', 'next_gif')
    # readonly_fields 


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','num_gifs', 'num_likes')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'gif_id','user_id', 'shocked', 'loved', 'laugh', 'like_date')

class HashtagAdmin(admin.ModelAdmin):
    list_display = ('hashtag', 'count')

class GifHashtagLinkerAdmin(admin.ModelAdmin):
    list_display = ('hashtag', 'gif')

class GifViewAdmin(admin.ModelAdmin):
    list_display = ('gif', 'user', 'ip_address', 'view_date')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Gif,  GifAdmin)
admin.site.register(Like,  LikeAdmin)
admin.site.register(Hashtag,  HashtagAdmin)
admin.site.register(GifHashtagLinker,  GifHashtagLinkerAdmin)
admin.site.register(GifView,  GifViewAdmin)