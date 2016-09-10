# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0002_premiumservice_category_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='contact_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='advert',
            name='contact_no',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
