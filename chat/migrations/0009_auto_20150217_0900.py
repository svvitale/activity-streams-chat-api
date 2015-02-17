# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20150217_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='msg',
            field=models.CharField(max_length=4000, verbose_name='message text', default=None),
            preserve_default=True,
        ),
    ]
