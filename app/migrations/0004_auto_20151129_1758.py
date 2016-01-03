# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20151129_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalconf',
            name='title',
            field=models.CharField(help_text='Please write your brand slogan', max_length=140, null=True, verbose_name=b'Brand slogan'),
            preserve_default=True,
        ),
    ]
