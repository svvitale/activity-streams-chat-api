# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import chat.models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20150215_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(verbose_name='time message sent', default=chat.models.get_now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(verbose_name='room name', default=None, unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.URLField(verbose_name='avatar url', default=None, blank=True, max_length=512),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_seen',
            field=models.DateTimeField(verbose_name='last time the user logged in', default=chat.models.get_now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='nick',
            field=models.CharField(verbose_name='user nickname', default=None, unique=True, max_length=100),
            preserve_default=True,
        ),
    ]
