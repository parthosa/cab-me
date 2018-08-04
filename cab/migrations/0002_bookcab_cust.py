# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
        ('cab', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcab',
            name='Cust',
            field=models.ManyToManyField(related_name=b'userprofile', null=True, to='registration.UserProfile'),
            preserve_default=True,
        ),
    ]
