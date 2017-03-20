from django.contrib import admin

from .models import Gif

class GifAdmin(admin.ModelAdmin):
    list_display = ('name', 'tags', 'upload_date', 'gif_path',)
    # exclude
    # readonly_fields 
admin.site.register(Gif, GifAdmin)
