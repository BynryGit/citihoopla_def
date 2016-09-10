# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0004_auto_20160829_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='country',
            field=models.ForeignKey(blank=True, to='digispaceapp.Country', null=True),
        ),
    ]
