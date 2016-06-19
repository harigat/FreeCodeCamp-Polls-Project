from django.shortcuts import render,redirect,get_object_or_404
from .models import Poll,Choice
from .forms import PollForm,MyModelFormSet
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
	return render(request,'polls/home.html')

def list(request):
	polls=Poll.objects.all().order_by('-pk')
	return render(request,'polls/list.html',{'polls':polls})

def detail(request,pk):
	poll=get_object_or_404(Poll,pk=pk)
	return render(request,'polls/detail.html',{'poll':poll})

def vote(request,pk):
	poll=get_object_or_404(Poll,pk=pk)
	try:
		selection=request.POST['choice']
		if selection != 'newchoice':
			choice=Choice.objects.get(pk=selection)
		else:
			choice=Choice.objects.create(poll=poll,choice=request.POST['newchoice'])
	except (KeyError,Choice.DoesNotExist):
		return render(request,'polls/detail.html',{'poll':poll,'error_message':'You didn\'t select a choice.'})
	else:
		choice.votes+=1
		choice.save()
		return render(request,'polls/detail.html',{'poll':poll})

@login_required
def create(request):
	if request.method=='POST':
		poll=PollForm(request.POST,prefix='pollf')
		choices=MyModelFormSet(request.POST,prefix='choicef')
		if poll.is_valid() and choices.is_valid():
			pollsaving=poll.save(commit=False)
			pollsaving.author=request.user
			pollsaving.save()
			for a in range(0,len(choices)):
				if choices[a].cleaned_data !={}:
					choices[a].instance.poll=pollsaving
					choices[a].save()
			return redirect('detail',pk=pollsaving.pk)
	else:
		poll=PollForm(prefix='pollf')
		choices=MyModelFormSet(queryset=Choice.objects.none(),prefix='choicef')
	return render(request,'polls/create.html',{'poll':poll,'choices':choices})

@login_required
def mypolls(request):
	polls=Poll.objects.filter(author=request.user)
	return render(request,'polls/list.html',{'polls':polls,'mypolls':True})
	
@login_required
def edit(request,pk):
	poll=get_object_or_404(Poll,pk=pk)
	if request.method=='POST':
		pollform=PollForm(request.POST,instance=poll,prefix='pollf')
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
		pollform=PollForm(prefix='pollf',instance=poll)
		choices=MyModelFormSet(queryset=poll.choice_set.all(),prefix='choicef')
	return render(request,'polls/edit.html',{'pollform':pollform,'choices':choices})