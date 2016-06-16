from django.db import models

# Create your models here.
class Poll(models.Model):
	author=models.ForeignKey('auth.User')
	question=models.CharField(max_length=200)
	def __str__(self):
		return self.question
		
class Choice(models.Model):
	question=models.ForeignKey('Poll',on_delete=models.CASCADE)
	choice=models.CharField(max_length=200)
	votes=models.IntegerField(default=0)
	def __str__(self):
		return self.choice