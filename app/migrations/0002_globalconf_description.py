# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalconf',
            name='description',
            field=models.TextField(help_text='Please describe in detail, what this site is about', null=True, verbose_name=b'Site Description'),
            preserve_default=True,
        ),
    ]
