# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('msg', models.CharField(max_length=4000, verbose_name='message text')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='time message sent')),
                ('room', models.ForeignKey(to='chat.Room')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nick', models.CharField(unique=True, max_length=100, verbose_name='user nickname')),
                ('avatar', models.URLField(max_length=512, verbose_name='avatar url')),
                ('last_seen', models.DateTimeField(auto_now_add=True, verbose_name='last time the user logged in')),
                ('active', models.BooleanField(default=True, verbose_name='user is currently logged in')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(to='chat.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='members',
            field=models.ManyToManyField(to='chat.User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(unique=True, max_length=100, verbose_name='room name'),
            preserve_default=True,
        ),
    ]
