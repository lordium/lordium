# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151013_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='fetch_status',
            field=models.IntegerField(default=1, choices=[(1, 'New'), (2, 'Fetching'), (3, 'Fetch Completed')]),
            preserve_default=True,
        ),
    ]
