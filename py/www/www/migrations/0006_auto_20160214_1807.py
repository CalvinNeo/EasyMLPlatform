# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0005_auto_20151217_0015'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'applyingtask',
            },
        ),
        migrations.AddField(
            model_name='mlmodel',
            name='model_path',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
