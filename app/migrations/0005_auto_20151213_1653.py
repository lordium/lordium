# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151129_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='location',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Location Coordinates'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='location_name',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Location Name'),
            preserve_default=True,
        ),
    ]
