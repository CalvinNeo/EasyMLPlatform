# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0006_auto_20160214_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessTask',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'assesstask',
            },
        ),
        migrations.AlterField(
            model_name='applytask',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
