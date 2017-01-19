# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20170118_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email_id',
            field=models.EmailField(unique=True, max_length=75),
            preserve_default=True,
        ),
    ]
