from django.shortcuts import render,redirect,get_object_or_404
from .models import Poll,Choice,Vote
from .forms import PollForm,MyModelFormSet,UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
import json
# Create your views here.
def home(request):
	return render(request,'polls/home.html')

def list(request):
	polls=Poll.objects.all().order_by('-pk')
	return render(request,'polls/list.html',{'polls':polls})

def detail(request,pk,error_message=False):
	poll=get_object_or_404(Poll,pk=pk)
	choice_set=poll.choice_set.all()
	choices=[x.choice for x in choice_set]
	votes=[x.votes for x in choice_set]
	return render(request,'polls/detail.html',{'poll':poll,'choices':json.dumps(choices),'votes':json.dumps(votes),'error_message':error_message})

def vote(request,pk):
	poll=get_object_or_404(Poll,pk=pk)
	user=request.user
	voted=request.COOKIES.get('voted_'+pk,False)
	if not voted and (str(user) is 'AnonymousUser' or not Vote.objects.filter(user=user,poll=poll).exists()):
		try:
			selection=request.POST['choice']
			new_choice=request.POST.get('newchoice')
			
			if selection != 'newchoice':
				choice=Choice.objects.get(pk=selection)
			elif user.is_authenticated():
				if new_choice.strip() is '':
					return detail(request,pk=pk,error_message='The textbox is empty')
				else:
					choice=Choice.objects.create(poll=poll,choice=request.POST['newchoice'])
			else:
				raise Choice.DoesNotExist
		except (KeyError,Choice.DoesNotExist):
			return detail(request,pk=pk,error_message='You didn\'t select a choice.')
		else:
			response=redirect('detail',pk=pk)
			response.set_cookie('voted_'+pk,True,max_age=10000)
			choice.votes+=1
			choice.save()
			if str(user) is not 'AnonymousUser':
				vote=Vote.objects.create(user=user,poll=poll)
			return response
	return detail(request,pk=pk,error_message='You have voted aleady.')

@login_required
def create(request):
	if request.method=='POST':
		pollform=PollForm(request.POST,prefix='pollf')
		choices=MyModelFormSet(request.POST,prefix='choicef')
		if pollform.is_valid() and choices.is_valid():
			poll=pollform.save(commit=False)
			poll.author=request.user
			poll.save()
			for a in range(0,len(choices)):
				if choices[a].cleaned_data !={}:
					choices[a].instance.poll=poll
					choices[a].save()
			return redirect('detail',pk=poll.pk)
	else:
		pollform=PollForm(prefix='pollf')
		choices=MyModelFormSet(queryset=Choice.objects.none(),prefix='choicef')
	return render(request,'polls/create.html',{'pollform':pollform,'choices':choices})

@login_required
def mypolls(request,error_message=None):
	polls=Poll.objects.filter(author=request.user)
	return render(request,'polls/list.html',{'polls':polls,'mypolls':True,'error_message':error_message})
	
@login_required
def edit(request,pk):
	poll=get_object_or_404(Poll,pk=pk)
	if request.method=='POST':
		pollform=PollForm(request.POST,instance=poll,prefix='pollf')
		choices=MyModelFormSet(request.POST,prefix='choicef')
		if pollform.is_valid() and choices.is_valid():
			poll.save()
			for a in range(0,len(choices)):
				if choices[a].cleaned_data !={}:
					choices[a].instance.poll=poll
					choices[a].save()
			return redirect('detail',pk=poll.pk)
	else:
		pollform=PollForm(prefix='pollf',instance=poll)
		choices=MyModelFormSet(queryset=poll.choice_set.all(),prefix='choicef')
	return render(request,'polls/edit.html',{'pollform':pollform,'choices':choices})
	
@login_required
def delete(request,pk):
	poll=get_object_or_404(Poll,pk=pk)
	if poll.author==request.user:
		poll.delete()
		return redirect('mypolls')
	return mypolls(request,error_message=True)
def register(request):
	if request.user.is_authenticated():
		return redirect('home')
	elif request.method=='POST':
		userform=UserForm(request.POST)
		if userform.is_valid():
			user=User.objects.create_user(**userform.cleaned_data)	
			a=userform.cleaned_data['password']
			b=request.POST['password']
			user=authenticate(username=user.username,password=userform.cleaned_data['password'])
			login(request,user)
			return redirect('home')
	else:
		userform=UserForm()
	return render(request,'registration/register.html',{'form':userform})