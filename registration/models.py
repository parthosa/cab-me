from django.db import models
from django.contrib.auth.models import User
from cab.models import *
from .models import *


class UserProfile(models.Model):

    stages = (
        ('0', 'nothing'),
        ('1', 'application downloaded'),
        ('2', 'invited 5'),
        ('3', 'invited 25'),
        ('4', 'invited 65'),
        ('5', 'invited 125'),
        )

    name = models.CharField('First Name', max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    phone = models.BigIntegerField(unique = True)
    email_id = models.EmailField(unique=True)
    user = models.OneToOneField(User, null=True)
    postedcabs = models.ManyToManyField(PostCab, blank = True, default = '')
    bookedcabs = models.ManyToManyField(BookCab, blank = True, default = '')
    rating = models.DecimalField(max_digits = 3, decimal_places = 2, null = True)
    invite_id = models.CharField(max_length = 20, null = True)
    invited_by = models.ForeignKey(User, null = True, related_name = 'invited_by')
    invites = models.ManyToManyField(User ,null = True, related_name = 'invites')
    app_downloaded = models.BooleanField(default = False)
    cabme_cash = models.BigIntegerField(default = 0)
    refer_stage = models.CharField(max_length = 30, choices = stages, default = '0')
    fbid = models.CharField(max_length = 70, null = True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.app_downloaded == False:
            self.refer_stage = '0'
        else:
            if len(self.invites.all()) < 5:
                self.refer_stage = '1'
            elif len(self.invites.all()) < 25:
                self.refer_stage = '2'
            elif len(self.invites.all()) < 65:
                self.refer_stage = '3'
            elif len(self.invites.all()) < 125:
                self.refer_stage = '4'
            else:
                self.refer_stage = '5'
        self.cabme_cash = 200*(int(self.refer_stage)+1)
        super(UserProfile, self).save(*args, **kwargs)



