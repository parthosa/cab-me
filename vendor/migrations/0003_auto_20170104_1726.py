# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-04 17:26
from __future__ import unicode_literals

from django.db import migrations, models
import vendor.models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_auto_20170101_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cab_type', models.CharField(choices=[(b'Sedan', b'Sedan'), (b'SUV', b'SUV'), (b'Hatchback', b'Hatchback')], max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='driver',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='proceeds',
            field=models.CharField(choices=[(b'OneWay', b'One Way'), (b'TwoWay', b'Two Way')], default=b'OneWay', max_length=50),
        ),
        migrations.AddField(
            model_name='vendor',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='proceeds',
            field=models.CharField(choices=[(b'OneWay', b'One Way'), (b'TwoWay', b'Two Way')], default=b'OneWay', max_length=50),
        ),
        migrations.AlterField(
            model_name='driver',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='cab',
            name='driver',
            field=models.OneToOneField(on_delete=vendor.models.Vendor, to='vendor.Driver'),
        ),
        migrations.AddField(
            model_name='driver',
            name='cabs',
            field=models.ManyToManyField(related_name='driver_cab', to='vendor.Cab'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='cabs',
            field=models.ManyToManyField(related_name='vendor_cab', to='vendor.Cab'),
        ),
    ]
