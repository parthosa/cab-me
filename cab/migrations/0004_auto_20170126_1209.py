# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cab', '0003_auto_20170126_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='hatch_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='sedan_price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='suv_price',
            field=models.IntegerField(null=True),
        ),
    ]
