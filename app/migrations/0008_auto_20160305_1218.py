# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20160305_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalconf',
            name='google_analytics',
            field=models.TextField(help_text='Google analytics script', verbose_name=b'Google Analytics', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='globalconf',
            name='keywords',
            field=models.TextField(help_text='Keywords for search engine', verbose_name=b'Keywords', blank=True),
            preserve_default=True,
        ),
    ]
