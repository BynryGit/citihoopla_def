# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('digispaceapp', '0006_auto_20160902_0623'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallerDetails',
            fields=[
                ('CallerID', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('first_name', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('last_name', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('IncomingTelNo', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('email', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('CallerArea', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('caller_created_date', models.DateTimeField(null=True, blank=True)),
                ('caller_created_by', models.CharField(max_length=100, null=True, blank=True)),
                ('caller_updated_by', models.CharField(max_length=100, null=True, blank=True)),
                ('caller_updated_date', models.DateTimeField(null=True, blank=True)),
                ('CallerCity', models.ForeignKey(blank=True, to='digispaceapp.City', null=True)),
                ('CallerPincode', models.ForeignKey(blank=True, to='digispaceapp.Pincode', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CallInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('UCID', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('CallerID', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('CalledNo', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('CallStartTime', models.DateTimeField(null=True, blank=True)),
                ('DialStartTime', models.DateTimeField(null=True, blank=True)),
                ('DialEndTime', models.DateTimeField(null=True, blank=True)),
                ('DisconnectType', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('CallStatus', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('CallDuration', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('CallType', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('AudioRecordingURL', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('DialedNumber', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('Department', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('Extn', models.CharField(default=None, max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnquiryDetails',
            fields=[
                ('EnquiryID', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('enquiryFor', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('SelectedArea', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('created_date', models.DateTimeField(null=True, blank=True)),
                ('created_by', models.CharField(max_length=100, null=True, blank=True)),
                ('updated_by', models.CharField(max_length=100, null=True, blank=True)),
                ('updated_date', models.DateTimeField(null=True, blank=True)),
                ('CallerID', models.ForeignKey(blank=True, to='digispaceapp.CallerDetails', null=True)),
                ('SelectedCity', models.ForeignKey(blank=True, to='digispaceapp.City', null=True)),
                ('SelectedPincode', models.ForeignKey(blank=True, to='digispaceapp.Pincode', null=True)),
                ('category_id', models.ForeignKey(blank=True, to='digispaceapp.Category', null=True)),
                ('subcategory_id1', models.ForeignKey(blank=True, to='digispaceapp.CategoryLevel1', null=True)),
                ('subcategory_id2', models.ForeignKey(blank=True, to='digispaceapp.CategoryLevel2', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, to=settings.AUTH_USER_MODEL)),
                ('operator_id', models.AutoField(serialize=False, editable=False, primary_key=True)),
                ('operator_name', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('operator_email_id', models.CharField(default=None, max_length=100, null=True, blank=True)),
                ('operator_status', models.CharField(default=b'1', max_length=100, null=True, choices=[(b'1', b'1'), (b'0', b'0')])),
                ('user_created_date', models.DateTimeField(null=True, blank=True)),
                ('user_created_by', models.CharField(max_length=100, null=True, blank=True)),
                ('user_updated_by', models.CharField(max_length=100, null=True, blank=True)),
                ('user_updated_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RenameField(
            model_name='supplier',
            old_name='country',
            new_name='country_id',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='city',
        ),
        migrations.AddField(
            model_name='consumerprofile',
            name='consumer_otp',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='area',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='city_place_id',
            field=models.ForeignKey(blank=True, to='digispaceapp.City_Place', null=True),
        ),
    ]
