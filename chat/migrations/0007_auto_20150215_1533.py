# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_auto_20150215_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(verbose_name='time message sent', default=datetime.datetime(2015, 2, 15, 22, 33, 1, 917548)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_seen',
            field=models.DateTimeField(verbose_name='last time the user logged in', default=datetime.datetime(2015, 2, 15, 22, 33, 1, 915548)),
            preserve_default=True,
        ),
    ]
