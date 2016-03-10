# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0003_mlmodel_classfeatureindex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingtask',
            name='datasetindex',
        ),
        migrations.RemoveField(
            model_name='trainingtask',
            name='datasetprototype',
        ),
        migrations.AddField(
            model_name='mlmodel',
            name='datasetindex',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mlmodel',
            name='datasetprototype',
            field=models.CharField(choices=[(b'LOCAL', b'LOCAL'), (b'ONLINE', b'ONLINE')], default='LOCAL', max_length=16),
            preserve_default=False,
        ),
    ]
