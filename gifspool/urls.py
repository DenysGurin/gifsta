from django.conf.urls import url

from . import views

app_name = 'gifspool'
urlpatterns = [
    url(r'^$', views.Pool.as_view(), name='gifspool'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]