from django.db import models
from django.contrib.auth.models import User
from cab.models import *

class Vendor(models.Model):
	name = models.CharField(max_length = 50, blank = False)
	contact = models.IntegerField(blank = False)
	email = models.EmailField(unique = True)
	user = models.OneToOneField(User, null = True)
	bookings = models.ForeignKey('cab.BookCab', related_name = 'vendor_book_cab')

	def __unicode__(self):
		return self.name

class Driver(models.Model):
	name = models.CharField(max_length = 50, blank = False)
	contact = models.IntegerField(blank = False)
	email = models.EmailField(unique = True)
	user = models.OneToOneField(User, null = True)
	bookings = models.ForeignKey('cab.BookCab', related_name = 'driver_book_cab')

	def __unicode__(self):
		return self.name	
