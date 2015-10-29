# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20151028_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.IntegerField(default=1, choices=[(1, 'Image'), (2, 'Video')]),
            preserve_default=True,
        ),
    ]
