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
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('path', models.FileField(upload_to=www.models.get_upload_to)),
                ('filetype', models.CharField(max_length=10)),
                ('head', models.CharField(max_length=1023)),
                ('attr_delim', models.CharField(max_length=3)),
                ('record_delim', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'dataset',
            },
        ),
        migrations.CreateModel(
            name='MLModel',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('modeltype', models.CharField(max_length=10)),
                ('path', models.FileField(upload_to=www.models.get_model_upload_to)),
            ],
            options={
                'db_table': 'models',
            },
        ),
    ]
