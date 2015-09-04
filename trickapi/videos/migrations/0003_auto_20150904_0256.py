# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20150904_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_id',
            field=models.CharField(unique=True, max_length=50, db_index=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_type',
            field=models.CharField(default=b'YT', max_length=2, choices=[(b'YT', b'YouTube'), (b'IG', b'Instagram'), (b'VN', b'Vine')]),
        ),
    ]
