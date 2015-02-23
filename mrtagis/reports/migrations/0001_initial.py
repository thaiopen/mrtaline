# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=75)),
                ('birth_date', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Checkin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('note', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('website', models.URLField()),
                ('logo', models.ImageField(upload_to=b'media', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('body', models.TextField()),
                ('slug', models.CharField(help_text=b'auto generate slug field', unique=True, max_length=200, blank=True)),
                ('publish', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=1, choices=[(b'd', b'Draft'), (b'p', b'Published'), (b'u', b'UnPublished')])),
                ('authors', models.ManyToManyField(to='reports.Author', blank=True)),
                ('contractor', models.ForeignKey(to='reports.Contractor', blank=True)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Report Entry',
                'verbose_name_plural': 'Report Entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('slug', models.CharField(max_length=256)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('description', models.TextField()),
                ('published', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('picture', models.ImageField(upload_to=b'')),
                ('status', models.CharField(max_length=1, choices=[(b'd', b'pending'), (b'p', b'confirm'), (b'a', b'approved')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlaceCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Place Category',
                'verbose_name_plural': 'Place Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Portal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('user', models.ForeignKey(related_name='lists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Portal',
                'verbose_name_plural': 'Portal',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('picture', models.ImageField(upload_to=b'reports/%Y/%m/%d', blank=True)),
                ('address', models.CharField(max_length=200, blank=True)),
                ('published', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(to='reports.Category', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReportArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('uuid', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='place',
            name='categories',
            field=models.ManyToManyField(to='reports.PlaceCategory', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='place',
            name='portal',
            field=models.ForeignKey(related_name='portals', to='reports.Portal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='place',
            name='user',
            field=models.ForeignKey(related_name='places', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='checkin',
            name='place',
            field=models.ForeignKey(to='reports.Place'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='checkin',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
