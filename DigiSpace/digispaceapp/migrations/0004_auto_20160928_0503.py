# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digispaceapp', '0003_telephoneenquiryratecard'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='category_level_1',
            field=models.ForeignKey(blank=True, to='digispaceapp.CategoryLevel1', null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='category_level_2',
            field=models.ForeignKey(blank=True, to='digispaceapp.CategoryLevel2', null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='category_level_3',
            field=models.ForeignKey(blank=True, to='digispaceapp.CategoryLevel3', null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='category_level_4',
            field=models.ForeignKey(blank=True, to='digispaceapp.CategoryLevel4', null=True),
        ),
        migrations.AddField(
            model_name='business',
            name='category_level_5',
            field=models.ForeignKey(blank=True, to='digispaceapp.CategoryLevel5', null=True),
        ),
    ]
