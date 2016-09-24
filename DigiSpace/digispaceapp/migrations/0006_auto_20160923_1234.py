# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0005_categorywiseratecard'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='user_name',
            new_name='user_first_name',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_last_name',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
    ]
