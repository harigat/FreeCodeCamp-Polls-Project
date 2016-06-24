from django import forms
from .models import Poll,Choice
from django.contrib.auth.models import User

class PollForm(forms.ModelForm):
	class Meta():
		model=Poll
		fields=('question',)

ChoiceFormset=forms.modelformset_factory(Choice,fields=('choice',),extra=0,min_num=2)
class MyModelFormSet(ChoiceFormset):
	def clean(self):
		super(MyModelFormSet, self).clean()
		a=[]
		for idx,form in enumerate(self.forms):
			if 'choice' in form.cleaned_data:
				choice = form.cleaned_data['choice']
				if choice not in a:
					a.append(choice)
				else:
					form.cleaned_data={}

class UserForm(forms.ModelForm):	
	repeat_password=forms.CharField(max_length=128,widget=forms.PasswordInput(),required=True)
	
	class Meta():
		model=User
		fields=('username','password','email')
		widgets={'password':forms.PasswordInput()}		

	def clean(self):
		cleaned_data=super(UserForm,self).clean()
		email = cleaned_data.get('email')
		username = cleaned_data.get('username')
		password=cleaned_data.get('password')
		repeat_password=cleaned_data.get('repeat_password')
		if not email:
			self.add_error('email','Please provide email address')
		elif User.objects.filter(email=email).exclude(username=username).count():
			self.add_error('email','Email addresses must be unique')
		
		if password and repeat_password and password != repeat_password:
			self.add_error('repeat_password','Passwords don\'t match')
		self.cleaned_data.pop('repeat_password',None)