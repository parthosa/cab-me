# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cab', '0002_bookcab_cust'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterCity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Price', models.IntegerField(default=7, null=True)),
                ('Type', models.CharField(max_length=50, null=True)),
                ('cab_id', models.CharField(max_length=50, null=True)),
                ('From', models.ForeignKey(related_name=b'inter_from', to='cab.City', null=True)),
                ('To', models.ForeignKey(related_name=b'inter_to', to='cab.City', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='city',
            name='hatch_price',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='sedan_price',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='city',
            name='suv_price',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bookcab',
            name='From',
            field=models.ForeignKey(related_name=b'book_from', to='cab.City', null=True),
        ),
        migrations.AlterField(
            model_name='bookcab',
            name='To',
            field=models.ForeignKey(related_name=b'book_to', to='cab.City', null=True),
        ),
        migrations.AlterField(
            model_name='cab',
            name='From',
            field=models.ForeignKey(related_name=b'cab_from', to='cab.City', null=True),
        ),
        migrations.AlterField(
            model_name='cab',
            name='To',
            field=models.ForeignKey(related_name=b'cab_to', to='cab.City', null=True),
        ),
        migrations.AlterField(
            model_name='postcab',
            name='From',
            field=models.ForeignKey(related_name=b'post_from', to='cab.City', null=True),
        ),
        migrations.AlterField(
            model_name='postcab',
            name='To',
            field=models.ForeignKey(related_name=b'post_to', to='cab.City', null=True),
        ),
    ]
