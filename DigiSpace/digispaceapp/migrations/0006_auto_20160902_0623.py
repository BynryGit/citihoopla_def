# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0005_supplier_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advert',
            name='currency_id',
        ),
        migrations.AddField(
            model_name='advert',
            name='country_id',
            field=models.ForeignKey(blank=True, to='digispaceapp.Country', null=True),
        ),
        migrations.AddField(
            model_name='advert',
            name='currency',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
