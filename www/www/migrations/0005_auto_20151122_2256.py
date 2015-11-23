# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0004_auto_20151122_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='mlmodel',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
