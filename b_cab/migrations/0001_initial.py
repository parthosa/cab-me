# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CabType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, choices=[(b'sedan', b'sedan'), (b'hatchback', b'hatchback'), (b'suv', b'suv')])),
                ('ac', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('uniqueID', models.CharField(max_length=20)),
                ('price_sedan_ac', models.IntegerField(default=0)),
                ('price_sedan_nac', models.IntegerField(default=0)),
                ('price_hatch_ac', models.IntegerField(default=0)),
                ('price_hatch_nac', models.IntegerField(default=0)),
                ('price_suv_ac', models.IntegerField(default=0)),
                ('price_suv_nac', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(related_name=b'company', to='b_cab.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
