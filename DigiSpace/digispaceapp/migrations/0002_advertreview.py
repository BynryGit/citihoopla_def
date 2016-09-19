# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertReview',
            fields=[
                ('id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('ratings', models.CharField(max_length=10, null=True, blank=True)),
                ('review', models.CharField(max_length=500, null=True, blank=True)),
                ('creation_date', models.DateTimeField(null=True, blank=True)),
                ('advert_id', models.ForeignKey(blank=True, to='digispaceapp.Advert', null=True)),
                ('user_id', models.ForeignKey(blank=True, to='digispaceapp.ConsumerProfile', null=True)),
            ],
        ),
    ]
