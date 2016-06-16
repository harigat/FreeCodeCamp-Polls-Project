from django.conf.urls import url
from . import views
urlpatterns=[
	url(r'^$',views.home,name='home'),
	url(r'^polls/$',views.list,name='list'),]
"""	
	url(r'^create/$',views.create,name='create'),
	url(r'^dashboard/$',views.dash,name='dash'),
	url(r'^login/$',views.login,name='login'),
	url(r'^logout/$',views.logout,name='logout'),
	url(r'^polls/(?P<pk>)$',views.detail,name='detail'),"""
