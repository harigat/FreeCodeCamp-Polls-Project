from django import forms
from .models import Poll,Choice
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