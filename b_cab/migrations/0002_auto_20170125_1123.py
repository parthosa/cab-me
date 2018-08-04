# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('b_cab', '0001_initial'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(related_name=b'userprof', to='registration.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='employees',
            field=models.ManyToManyField(related_name=b'employee', to='b_cab.Employee'),
            preserve_default=True,
        ),
    ]
