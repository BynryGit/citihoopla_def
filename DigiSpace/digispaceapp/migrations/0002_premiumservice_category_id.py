# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='premiumservice',
            name='category_id',
            field=models.ForeignKey(blank=True, to='digispaceapp.Category', null=True),
        ),
    ]
