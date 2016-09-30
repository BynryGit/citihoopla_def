# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0004_auto_20160928_0503'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnquiryService',
            fields=[
                ('enquiry_service_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('enquiry_service_name', models.CharField(max_length=30)),
                ('no_of_days', models.CharField(max_length=30)),
                ('category_id', models.CharField(max_length=10, null=True, blank=True)),
                ('category_level', models.CharField(max_length=10, null=True, blank=True)),
                ('start_date', models.CharField(max_length=30, null=True, blank=True)),
                ('end_date', models.CharField(max_length=30, null=True, blank=True)),
                ('enquiry_service_status', models.CharField(default=b'1', max_length=15, null=True, blank=True, choices=[(b'1', b'1'), (b'0', b'0')])),
                ('enquiry_service_created_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('enquiry_service_created_by', models.CharField(max_length=30, null=True, blank=True)),
                ('enquiry_service_updated_by', models.CharField(max_length=30, null=True, blank=True)),
                ('enquiry_service_updated_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='premiumservice',
            name='category_level',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='is_active',
            field=models.CharField(default=b'1', max_length=2, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='premiumservice',
            name='category_id',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='enquiryservice',
            name='business_id',
            field=models.ForeignKey(blank=True, to='digispaceapp.Business', null=True),
        ),
    ]
