# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-05 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '0001_initial'),
        ('cab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcab',
            name='Cust',
            field=models.ManyToManyField(related_name='userprofile', to='registration.UserProfile'),
        ),
    ]
