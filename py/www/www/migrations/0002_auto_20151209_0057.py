# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlmodel',
            name='modelstatus',
            field=models.CharField(choices=[(b'INITED', b'INITED'), (b'TRAINING', b'TRAINING'), (b'TRAINED', b'TRAINED')], max_length=32),
        ),
        migrations.AlterField(
            model_name='mlmodel',
            name='modeltype',
            field=models.CharField(max_length=32),
        ),
    ]
