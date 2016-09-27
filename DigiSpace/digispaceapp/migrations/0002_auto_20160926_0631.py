# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='sales_person_contact_number',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='sales_person_email',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='sales_person_name',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
    ]
