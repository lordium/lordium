# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20151213_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalconf',
            name='keywords',
            field=models.TextField(help_text='Keywords for search engine', null=True, verbose_name=b'Keywords'),
            preserve_default=True,
        ),
    ]
