# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-03 16:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cab', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostCab',
            new_name='Cab',
        ),
    ]
