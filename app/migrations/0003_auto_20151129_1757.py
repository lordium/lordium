# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_globalconf_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalconf',
            name='title',
            field=models.TextField(help_text='Please write your brand slogan', null=True, verbose_name=b'Brand slogan'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='globalconf',
            name='description',
            field=models.TextField(help_text='Please describe your brand, this will be used by \t\t\tsearch engines', null=True, verbose_name=b'Brand description'),
            preserve_default=True,
        ),
    ]
