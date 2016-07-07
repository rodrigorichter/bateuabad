from django.conf.urls import url
from . import views

app_name = 'board'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^addthread/$', views.addthread, name='addthread'),
    url(r'^(?P<pk>\d+)/addcomment/$', views.addcomment, name='addcomment'),
]