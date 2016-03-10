# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0002_auto_20151209_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='mlmodel',
            name='classfeatureindex',
            field=models.IntegerField(default=-1),
        ),
    ]
