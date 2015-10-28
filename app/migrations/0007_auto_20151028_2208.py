# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20151028_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_type',
            field=models.IntegerField(default=1, choices=[(b'image', 'Image'), (b'video', 'Video')]),
            preserve_default=True,
        ),
    ]
