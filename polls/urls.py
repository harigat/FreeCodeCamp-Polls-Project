from django.conf.urls import url
from . import views
urlpatterns=[
	url(r'^$',views.home,name='home'),
	url(r'^polls/$',views.list,name='list'),
	url(r'^polls/(?P<pk>[0-9]+)$',views.detail,name='detail'),
	url(r'^polls/(?P<pk>[0-9]+)/vote$',views.vote,name='vote'),
#	url(r'^mypolls/$',views.mypolls,name='mypolls'),
	url(r'^create/$',views.create,name='create'),
]
