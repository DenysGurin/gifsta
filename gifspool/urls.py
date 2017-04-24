from django.conf.urls import url

from . import views

app_name = 'gifspool'
urlpatterns = [
    url(r'^$', views.Pool.as_view(), name='gifspool'),
    url(r'^login/', views.Login.as_view(), name='login'),
    url(r'^logout/', views.Logout.as_view(), name='logout'),
    url(r'^(?P<pk>[0-9]+)/$', views.OneGif.as_view(), name='onegif'),
    url(r'^tags/(?P<tags>#\w+)/$', views.Tags.as_view(), name='tags'),
    url(r'^(?P<pk>[0-9]+)/shocked/$', views.shocked, name='shocked'),
    url(r'^(?P<pk>[0-9]+)/loved/$', views.loved, name='loved'),
    url(r'^(?P<pk>[0-9]+)/laugh/$', views.laugh, name='laugh'),
    url(r'^upload/', views.Upload.as_view(), name='upload'),
]