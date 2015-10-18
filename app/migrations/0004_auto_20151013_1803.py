# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20151010_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_picture',
            field=models.TextField(null=True, validators=[django.core.validators.URLValidator()]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='media_id',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
