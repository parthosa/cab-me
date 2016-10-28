from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import *
from cab.models import *


class UserProfile(models.Model):
    name = models.CharField('First Name', max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email_id = models.EmailField(unique=True)
    user = models.OneToOneField(User, SocialAccount, null=True)
    postedcabs = models.ManyToManyField(PostCab, blank = True, default = '')
    bookedcabs = models.ManyToManyField(BookCab, blank = True, default = '')
    rating = models.DecimalField(max_digits = 3, decimal_places = 2, null = True)
    def __unicode__(self):
        return self.name

