from django.contrib import admin

from .models import Gif, Category

class GifAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator','name', 'tags', 'upload_date')
    # exclude
    # readonly_fields 
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name','num_gifs', 'num_likes')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Gif,  GifAdmin)