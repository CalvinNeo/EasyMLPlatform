# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import www.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('path', models.FileField(upload_to=www.models.get_upload_to)),
                ('filetype', models.CharField(max_length=10)),
                ('head', models.CharField(default=b'', max_length=1023)),
                ('attr_delim', models.CharField(max_length=3)),
                ('record_delim', models.CharField(max_length=3)),
                ('hashead', models.BooleanField(default=True)),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name=b'create time')),
            ],
            options={
                'db_table': 'dataset',
            },
        ),
        migrations.CreateModel(
            name='MLModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('modeltype', models.CharField(choices=[(b'INITED', b'INITED'), (b'TRAINING', b'TRAINING'), (b'TRAINED', b'TRAINED')], max_length=32)),
                ('modelstatus', models.CharField(max_length=32)),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name=b'create time')),
            ],
            options={
                'db_table': 'models',
            },
        ),
        migrations.CreateModel(
            name='OnlineDataset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('head', models.CharField(default=b'', max_length=1023)),
                ('url', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=1023)),
                ('search', models.CharField(max_length=1023)),
                ('renewstrategy', models.CharField(max_length=32)),
                ('hashead', models.BooleanField(default=True)),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name=b'create time')),
            ],
            options={
                'db_table': 'onlinefield',
            },
        ),
        migrations.CreateModel(
            name='TrainingTask',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('modelprototype', models.CharField(max_length=32)),
                ('datasetprototype', models.CharField(choices=[(b'LOCAL', b'LOCAL'), (b'ONLINE', b'ONLINE')], max_length=16)),
                ('modelindex', models.IntegerField()),
                ('datasetindex', models.IntegerField()),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name=b'create time')),
            ],
            options={
                'db_table': 'trainingtask',
            },
        ),
    ]
