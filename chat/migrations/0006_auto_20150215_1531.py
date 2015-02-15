# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_auto_20150215_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 15, 22, 31, 5, 604705), verbose_name='time message sent'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_seen',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 15, 22, 31, 5, 602705), verbose_name='last time the user logged in'),
            preserve_default=True,
        ),
    ]
