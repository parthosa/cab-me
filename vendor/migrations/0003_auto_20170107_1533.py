# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import vendor.models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_auto_20170107_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cab',
            name='driver',
            field=models.OneToOneField(to='vendor.Driver', to_field=vendor.models.Vendor),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='driver',
            name='email',
            field=models.EmailField(max_length=75, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vendor',
            name='email',
            field=models.EmailField(max_length=75, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
