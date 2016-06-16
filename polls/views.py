from django.shortcuts import render,redirect
from .models import Poll
# Create your views here.
def home(request):
	return render(request,'polls/home.html')
	
def list(request):
	polls=Poll.objects.all().order_by('-pk')
	return render(request,'polls/list.html',{'polls':polls})