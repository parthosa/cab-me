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
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'First Name')),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=100)),
                ('phone', models.BigIntegerField(unique=True)),
                ('email_id', models.EmailField(unique=True, max_length=75)),
                ('rating', models.DecimalField(null=True, max_digits=3, decimal_places=2)),
                ('invite_id', models.CharField(max_length=20, null=True)),
                ('app_downloaded', models.BooleanField(default=False)),
                ('cabme_cash', models.BigIntegerField(default=0)),
                ('refer_stage', models.CharField(default=b'0', max_length=30, choices=[(b'0', b'nothing'), (b'1', b'application downloaded'), (b'2', b'invited 5'), (b'3', b'invited 25'), (b'4', b'invited 65'), (b'5', b'invited 125')])),
                ('fbid', models.CharField(max_length=70, null=True)),
                ('bookedcabs', models.ManyToManyField(default=b'', to='cab.BookCab', blank=True)),
                ('invited_by', models.ForeignKey(related_name=b'invited_by', to=settings.AUTH_USER_MODEL, null=True)),
                ('invites', models.ManyToManyField(related_name=b'invites', null=True, to=settings.AUTH_USER_MODEL)),
                ('postedcabs', models.ManyToManyField(default=b'', to='cab.PostCab', blank=True)),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
