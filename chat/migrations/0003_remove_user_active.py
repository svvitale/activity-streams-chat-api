# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20150213_0031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='active',
        ),
    ]
