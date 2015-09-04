# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_type',
            field=models.CharField(default=b'YT', unique=True, max_length=2, db_index=True, choices=[(b'YT', b'YouTube'), (b'IG', b'Instagram'), (b'VN', b'Vine')]),
        ),
    ]
