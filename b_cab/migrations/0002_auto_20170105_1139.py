# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-05 11:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('b_cab', '0001_initial'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprof', to='registration.UserProfile'),
        ),
        migrations.AddField(
            model_name='company',
            name='employees',
            field=models.ManyToManyField(related_name='employee', to='b_cab.Employee'),
        ),
    ]