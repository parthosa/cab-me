# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import allauth.socialaccount.models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20161230_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(null=True, to_field=allauth.socialaccount.models.SocialAccount, to=settings.AUTH_USER_MODEL),
        ),
    ]
