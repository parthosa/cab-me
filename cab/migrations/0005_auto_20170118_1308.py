# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-18 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cab', '0004_auto_20170118_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookcab',
            name='Cust',
            field=models.ManyToManyField(null=True, related_name='userprofile', to='registration.UserProfile'),
        ),
    ]
