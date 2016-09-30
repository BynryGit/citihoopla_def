# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0002_auto_20160926_0631'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelephoneEnquiryRateCard',
            fields=[
                ('rate_card_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('service_name', models.CharField(max_length=30)),
                ('cost_for_3_days', models.CharField(max_length=30, null=True, blank=True)),
                ('cost_for_7_days', models.CharField(max_length=30, null=True, blank=True)),
                ('cost_for_30_days', models.CharField(max_length=30, null=True, blank=True)),
                ('cost_for_90_days', models.CharField(max_length=30, null=True, blank=True)),
                ('cost_for_180_days', models.CharField(max_length=30, null=True, blank=True)),
                ('rate_card_status', models.CharField(default=b'1', max_length=15, null=True, blank=True, choices=[(b'1', b'1'), (b'0', b'0')])),
                ('rate_card_created_date', models.DateTimeField(null=True, blank=True)),
                ('rate_card_created_by', models.CharField(max_length=30, null=True, blank=True)),
                ('rate_card_updated_by', models.CharField(max_length=30, null=True, blank=True)),
                ('rate_card_updated_date', models.DateTimeField(null=True, blank=True)),
                ('city_place_id', models.ForeignKey(blank=True, to='digispaceapp.City_Place', null=True)),
            ],
        ),
    ]
