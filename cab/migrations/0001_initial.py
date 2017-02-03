# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('From', models.CharField(max_length=100, choices=[(b'test', b'test')])),
                ('To', models.CharField(max_length=100, choices=[(b'test', b'test')])),
                ('Date', models.CharField(max_length=10)),
                ('Date_return', models.CharField(default=b'', max_length=10)),
                ('Time', models.CharField(max_length=10)),
                ('Oneway', models.BooleanField(default=True)),
                ('Price', models.IntegerField()),
                ('Type', models.CharField(max_length=20)),
                ('Sharing', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('From', models.CharField(blank=True, max_length=100, null=True, choices=[(b'test', b'test')])),
                ('To', models.CharField(blank=True, max_length=100, null=True, choices=[(b'test', b'test')])),
                ('DriverName', models.CharField(default=b'', max_length=100)),
                ('Date', models.CharField(max_length=10, null=True, blank=True)),
                ('Date_return', models.CharField(default=b'', max_length=10, null=True, blank=True)),
                ('Time', models.CharField(max_length=10, blank=True)),
                ('Type', models.CharField(max_length=20)),
                ('cab_id', models.CharField(default=b'', max_length=1000)),
                ('price', models.IntegerField(default=7)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostCab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('From', models.CharField(max_length=100, choices=[(b'test', b'test')])),
                ('To', models.CharField(max_length=100, choices=[(b'test', b'test')])),
                ('Date', models.CharField(max_length=10)),
                ('Date_return', models.CharField(default=b'', max_length=10)),
                ('Time', models.CharField(max_length=10)),
                ('Type', models.CharField(max_length=20)),
                ('Smoking', models.BooleanField(default=False)),
                ('Pet', models.BooleanField(default=False)),
                ('Music', models.BooleanField(default=False)),
                ('SeatsAvail', models.IntegerField(default=2)),
                ('price', models.IntegerField(default=0)),
                ('cab_id', models.CharField(default=b'', max_length=1000)),
                ('user', models.ForeignKey(default=b'', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
