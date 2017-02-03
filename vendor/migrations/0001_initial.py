# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cab', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cab_type', models.CharField(max_length=50, choices=[(b'Sedan', b'Sedan'), (b'SUV', b'SUV'), (b'Hatchback', b'Hatchback')])),
                ('cab_number', models.CharField(max_length=60, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('contact', models.IntegerField()),
                ('email', models.EmailField(max_length=75, unique=True, null=True, blank=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('proceeds', models.CharField(default=b'OneWay', max_length=50, choices=[(b'OneWay', b'One Way'), (b'TwoWay', b'Two Way')])),
                ('bookings', models.ForeignKey(related_name=b'driver_book_cab', to='cab.BookCab', null=True)),
                ('cabs', models.ManyToManyField(related_name=b'driver_cab', to='vendor.Cab')),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('contact', models.IntegerField()),
                ('email', models.EmailField(max_length=75, unique=True, null=True, blank=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('proceeds', models.CharField(default=b'OneWay', max_length=50, choices=[(b'OneWay', b'One Way'), (b'TwoWay', b'Two Way')])),
                ('bookings', models.ForeignKey(related_name=b'vendor_book_cab', to='cab.BookCab', null=True)),
                ('cabs', models.ManyToManyField(related_name=b'vendor_cab', to='vendor.Cab')),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cab',
            name='driver',
            field=models.ForeignKey(to='vendor.Driver', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cab',
            name='vendor',
            field=models.ForeignKey(to='vendor.Vendor', null=True),
            preserve_default=True,
        ),
    ]
