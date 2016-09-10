# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0003_auto_20160826_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='discounts_status',
            field=models.CharField(default=b'true', max_length=100, null=True, choices=[(b'true', b'true'), (b'false', b'false')]),
        ),
        migrations.AddField(
            model_name='supplier',
            name='no_call_status',
            field=models.CharField(default=b'true', max_length=100, null=True, choices=[(b'true', b'true'), (b'false', b'false')]),
        ),
        migrations.AddField(
            model_name='supplier',
            name='notification_status',
            field=models.CharField(default=b'true', max_length=100, null=True, choices=[(b'true', b'true'), (b'false', b'false')]),
        ),
        migrations.AddField(
            model_name='supplier',
            name='reminders_status',
            field=models.CharField(default=b'true', max_length=100, null=True, choices=[(b'true', b'true'), (b'false', b'false')]),
        ),
        migrations.AddField(
            model_name='supplier',
            name='request_call_back_status',
            field=models.CharField(default=b'true', max_length=100, null=True, choices=[(b'true', b'true'), (b'false', b'false')]),
        ),
    ]
