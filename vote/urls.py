from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views
from polls.views import register
urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'', include('polls.urls')),
	url(r'^login/$',views.login,name='login'),
	url(r'^logout/$',views.logout,name='logout',kwargs={'next_page': '/'}),
	url(r'^register/$',register,name='register'),
]
