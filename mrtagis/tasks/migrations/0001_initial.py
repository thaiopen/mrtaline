# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('body', models.TextField()),
                ('taskid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('slug', models.CharField(help_text=b'auto generate slug field', unique=True, max_length=200, blank=True)),
                ('state', django_fsm.FSMField(default=b'new', max_length=50)),
                ('priority', models.IntegerField(default=2, choices=[(1, b'Low'), (2, b'Normal'), (3, b'High')])),
                ('assign_date', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('due_date', models.DateTimeField(default=None)),
                ('staff', models.ForeignKey(to='tasks.Staff', blank=True)),
            ],
            options={
                'ordering': ['-assign_date'],
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
            bases=(models.Model,),
        ),
    ]
