# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-07 11:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='bookings',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver_book_cab', to='cab.BookCab'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='bookings',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_book_cab', to='cab.BookCab'),
        ),
    ]
