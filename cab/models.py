from django.db import models
from django.contrib.auth.models import User
from registration.models import *


cities = (
	('test', 'test'),
	)
class BookCab(models.Model):

	From = models.CharField(max_length = 100, choices=cities, blank = False)
	To = models.CharField(max_length = 100, choices=cities, blank = False)
	Date = models.DateField(blank = False)
	Time = models.CharField(max_length = 10)
	Oneway = models.BooleanField(default = True)
	Price = models.IntegerField()
	Type = models.CharField(max_length=20)
	Sharing = models.BooleanField(default=False)
	Cust = models.ManyToManyField(User) 

	def __unicode__(self):
		return self.id

class Cab(models.Model):
	From = models.CharField(max_length = 100, choices=cities, blank = False)
	To = models.CharField(max_length = 100, choices=cities, blank = False)
	DriverName = models.CharField(max_length = 100, blank = False, default = '')
	Date = models.DateField(blank = False)
	Time = models.CharField(max_length = 10)
	Type = models.CharField(max_length=20)	
	cab_id = models.CharField(max_length = 1000, default = '')

	def __unicode__(self):
		return self.id

class PostCab(models.Model):
	From = models.CharField(max_length = 100, choices=cities, blank = False)
	To = models.CharField(max_length = 100, choices=cities, blank = False)
	Date = models.DateField(blank = False)
	Time = models.CharField(max_length = 10)
	Type = models.CharField(max_length=20)	
	Smoking = models.BooleanField(default = False)
	Pet = models.BooleanField(default = False)
	Music = models.BooleanField(default = False)
	SeatsAvail = models.IntegerField(default = 2)
	user = models.ForeignKey(User, blank = False, default = '')
	price = models.IntegerField(default = 0, blank = False)
	cab_id = models.CharField(max_length = 1000, default = '') #when posting the cab save this object by appending a character 'p' in front of the auto id of this object

	def __unicode__(self):
		return self.id		

	