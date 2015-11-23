# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0005_auto_20151122_2256'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineDataset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('url', models.URLField()),
                ('location', models.CharField(max_length=1023)),
                ('search', models.CharField(max_length=1023)),
            ],
            options={
                'db_table': 'onlinefield',
            },
        ),
    ]
