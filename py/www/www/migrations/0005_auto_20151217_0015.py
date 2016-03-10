# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0004_auto_20151211_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlmodel',
            name='loss',
            field=models.CharField(choices=[(b'QUAD', b'QUAD'), (b'BIN', b'BIN'), (b'ABS', b'ABS'), (b'LOG', b'LOG')], default=b'QUAD', max_length=20),
        ),
        migrations.AddField(
            model_name='mlmodel',
            name='negative',
            field=models.FloatField(default=-0.5),
        ),
        migrations.AddField(
            model_name='mlmodel',
            name='positive',
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name='mlmodel',
            name='classfeatureindex',
            field=models.IntegerField(),
        ),
    ]
