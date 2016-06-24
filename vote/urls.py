from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from polls.views import register
urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'', include('polls.urls')),
	url(r'^login/$',views.login,name='login'),
	url(r'^logout/$',views.logout,name='logout'),
	url(r'^register/$',register,name='register'),
#	url('^register/', CreateView.as_view(
#            template_name='registration/register.html',
 #           form_class=UserCreationForm,
 #           success_url='/'
#    )),
 #   url('^accounts/', include('django.contrib.auth.urls')),
]
