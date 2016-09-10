# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0007_auto_20160908_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertCallbacks',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('creation_date', models.DateTimeField(null=True, blank=True)),
                ('advert_id', models.ForeignKey(blank=True, to='digispaceapp.Advert', null=True)),
                ('user_id', models.ForeignKey(blank=True, to='digispaceapp.ConsumerProfile', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdvertCallsMade',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('creation_date', models.DateTimeField(null=True, blank=True)),
                ('advert_id', models.ForeignKey(blank=True, to='digispaceapp.Advert', null=True)),
                ('user_id', models.ForeignKey(blank=True, to='digispaceapp.ConsumerProfile', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdvertShares',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('creation_date', models.DateTimeField(null=True, blank=True)),
                ('advert_id', models.ForeignKey(blank=True, to='digispaceapp.Advert', null=True)),
                ('user_id', models.ForeignKey(blank=True, to='digispaceapp.ConsumerProfile', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AdvertView',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('creation_date', models.DateTimeField(null=True, blank=True)),
                ('advert_id', models.ForeignKey(blank=True, to='digispaceapp.Advert', null=True)),
                ('user_id', models.ForeignKey(blank=True, to='digispaceapp.ConsumerProfile', null=True)),
            ],
        ),
    ]
