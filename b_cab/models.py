from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import *
from cab.models import *
from registration.models import *


class Company(models.Model):
	name = models.CharField(max_length = 100)
	uniqueID = models.CharField(max_length = 20)
	employees = models.ManyToManyField('Employee', related_name = 'employee')
	price_sedan_ac = models.IntegerField(default = 0) #price of sedan ac
	price_sedan_nac = models.IntegerField(default = 0) #priceof sedan non ac
	price_hatch_ac = models.IntegerField(default = 0)
	price_hatch_nac = models.IntegerField(default = 0)
	price_suv_ac = models.IntegerField(default = 0)
	price_suv_nac = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.name

class Employee(models.Model):
	user = models.ForeignKey( 'registration.UserProfile', related_name = 'userprof')
	company = models.ForeignKey('Company', related_name = 'company')
	# bookings = models.ManyToManyField('Bcab', related_name = 'bcab')

	def __unicode__(self):
		return self.user.name

# class bcab(models.Model):
# 	name = models.CharField(max_length = 100)
# 	cab_type = models.ForeignKey('CabType', related_name = 'cabtype')

class CabType(models.Model):
	cabtype = (
				('sedan', 'sedan'),
				('hatchback', 'hatchback'),
				('suv', 'suv')
				)
	name = models.CharField(max_length = 10, choices = cabtype)
	ac = models.BooleanField(default = False)

	def __unicode__(self):
		return self.name	

