# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('insta_id', models.CharField(max_length=140, unique=True, null=True)),
                ('insta_token', models.TextField(null=True, verbose_name=b'Token')),
                ('profile_picture', models.TextField(null=True, validators=[django.core.validators.URLValidator()])),
                ('slogan', models.CharField(max_length=140, null=True)),
                ('fetch_status', models.IntegerField(default=0, help_text='Shows account status for fetching posts', choices=[(0, 'Not Registered'), (1, 'New'), (2, 'Fetching'), (3, 'Fetch Completed'), (4, 'Need Fetch')])),
                ('read_only', models.BooleanField(default=False, help_text='Allows read only on all resources', verbose_name=b'Read only')),
                ('is_brand', models.BooleanField(default=False, help_text='This account will be displayed on front page', verbose_name=b'Is Brand')),
            ],
            options={
                'verbose_name': 'Account',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='GlobalConf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instagram_app_id', models.CharField(help_text='Instagram app id (Client id)', max_length=140, verbose_name=b'App id')),
                ('instagram_app_secret', models.CharField(help_text='Instagram app secret (Client Secret)', max_length=140, verbose_name=b'App Secret')),
                ('google_analytics', models.TextField(help_text='Google analytics script', null=True, verbose_name=b'Google Analytics')),
                ('total_posts', models.IntegerField(default=0, verbose_name=b'Total Posts')),
                ('total_accounts', models.IntegerField(default=0, verbose_name=b'Total Accounts')),
                ('last_fetched', models.DateTimeField(null=True, verbose_name=b'Last Fetched')),
                ('website_url', models.CharField(max_length=140, null=True, verbose_name=b'Website URL')),
                ('insta_connected', models.BooleanField(default=False, verbose_name=b'App connected')),
            ],
            options={
                'verbose_name': 'Setting',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('media_id', models.CharField(max_length=200, null=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('date_published', models.DateTimeField(verbose_name=b'Date Published')),
                ('post_type', models.IntegerField(default=1, choices=[(1, 'Image'), (2, 'Video')])),
                ('post_url', models.TextField(null=True, validators=[django.core.validators.URLValidator()])),
                ('description', models.TextField(null=True, verbose_name=b'Description')),
                ('post_tags', models.TextField(null=True, verbose_name=b'Tags')),
                ('location', models.TextField(null=True, verbose_name=b'Location Coordinates')),
                ('location_name', models.TextField(null=True, verbose_name=b'Location Name')),
                ('account', models.ForeignKey(to='app.Account', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
