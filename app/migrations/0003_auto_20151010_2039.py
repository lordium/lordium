# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='insta_id',
            field=models.CharField(max_length=140, unique=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='insta_token',
            field=models.TextField(null=True, verbose_name=b'Token'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='account',
            field=models.ForeignKey(to='app.Account', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(null=True, verbose_name=b'Description'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='location',
            field=models.TextField(null=True, verbose_name=b'Location Coordinates'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='location_name',
            field=models.TextField(null=True, verbose_name=b'Location Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='post_tags',
            field=models.TextField(null=True, verbose_name=b'Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.IntegerField(default=1, choices=[(1, 'Image'), (2, 'Video')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='post_url',
            field=models.TextField(null=True, validators=[django.core.validators.URLValidator()]),
            preserve_default=True,
        ),
    ]
