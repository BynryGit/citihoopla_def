# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0003_ratecard'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ratecard',
            old_name='card_updated_by',
            new_name='rate_card_updated_by',
        ),
    ]
