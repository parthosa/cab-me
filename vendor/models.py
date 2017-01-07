from django.db import models
from django.contrib.auth.models import User
from cab.models import *


class Vendor(models.Model):
	ways = (
		('OneWay', 'One Way'),
		('TwoWay', 'Two Way'),
	)

	name = models.CharField(max_length = 50, blank = False)
	contact = models.IntegerField(blank = False)
	email = models.EmailField(unique = True, blank = True, null = True)
	user = models.OneToOneField(User, null = True)
	bookings = models.ForeignKey('cab.BookCab', related_name = 'vendor_book_cab', null = True)
	date_of_birth = models.DateField(null = True)
	proceeds = models.CharField(choices = ways, max_length = 50 , default = 'OneWay')
	cabs = models.ManyToManyField('Cab', related_name = 'vendor_cab')

	def __unicode__(self):
		return self.name

class Driver(models.Model):
	ways = (
		('OneWay', 'One Way'),
		('TwoWay', 'Two Way'),
	)
	name = models.CharField(max_length = 50, blank = False)
	contact = models.IntegerField(blank = False)
	email = models.EmailField(unique = True, blank = True, null = True)
	user = models.OneToOneField(User, null = True)
	bookings = models.ForeignKey('cab.BookCab', related_name = 'driver_book_cab', null = True)
	date_of_birth = models.DateField(null = True)
	proceeds = models.CharField(choices = ways, max_length = 50 , default = 'OneWay')
	cabs = models.ManyToManyField('Cab', related_name = 'driver_cab')

	def __unicode__(self):
		return self.name

class Cab(models.Model):
	cab_type = (
		('Sedan', 'Sedan'),
		('SUV', "SUV"),
		('Hatchback', 'Hatchback')
		)
	cab_type = models.CharField(choices = cab_type, max_length = 50)	
	driver = models.OneToOneField(Driver, Vendor)
	cab_number = models.CharField(max_length = 60, null = True)

	def __unicode__(self):
		return self.driver.name