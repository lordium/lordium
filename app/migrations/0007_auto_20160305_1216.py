# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_globalconf_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalconf',
            name='google_analytics',
            field=models.TextField(default=False, help_text='Google analytics script', verbose_name=b'Google Analytics'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='globalconf',
            name='keywords',
            field=models.TextField(default=False, help_text='Keywords for search engine', verbose_name=b'Keywords'),
            preserve_default=True,
        ),
    ]
