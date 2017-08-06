from django.conf.urls import url

from . import views
from .models import Category

categories = "|".join([category.name for category in Category.objects.all()])
app_name = 'gifspool'
urlpatterns = [
    url(r'^$', views.Pool.as_view(), name='gifspool'),

    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),

    url(r'^(?P<pk>[^/]+)-(?P<name>[^/]+)/$', views.OneGif.as_view(), name='onegif'),

    url(r'^search$', views.Tags.as_view(), name='tags'),#(?P<tags>\w+)
    url(r'^gifs/(?P<pk>[^/]+)-(?P<name>[^/]+)/$', views.Gifs.as_view(), name='gifs'),#(?P<tags>\w+)

    url(r'^categories/(?P<category>%s)/$'%categories, views.CategoriesGifs.as_view(), name='categoriesgifs'),

    url(r'^(?P<pk>[0-9]+)-(?P<name>[^/]+)/shocked/$', views.shocked, name='shocked'),
    url(r'^(?P<pk>[0-9]+)-(?P<name>[^/]+)/loved/$', views.loved, name='loved'),
    url(r'^(?P<pk>[0-9]+)-(?P<name>[^/]+)/laugh/$', views.laugh, name='laugh'),


    #AJAX
    url(r'^likes_ajax/$', views.likes_ajax, name='likes_ajax'),

    # url(r'^shocked/$', views.shocked_ajax, name='shocked_ajax'),
    # url(r'^loved/$', views.loved_ajax, name='loved_ajax'),
    # url(r'^laugh/$', views.laugh_ajax, name='laugh_ajax'),


    url(r'^upload/$', views.Upload.as_view(), name='upload'),

    url(r'^best/(?P<period>day|week|month)/$', views.Best.as_view(), name='best_by'),

    url(r'^cache/$', views.see_cache, name='see_cache'),

    url(r'^add_ajax/$', views.add_ajax),
    url(r'^ajax/$', views.ajax),

    url(r'^cookies/$', views.cookies_page),
	url(r'^set_cookies/$', views.set_cookies),
    
	url(r'^session/$', views.session_page),
	url(r'^set_session/$', views.set_session),

    url(r'^goToMp4/$', views.goToMp4),
]