# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_type', models.CharField(default=b'YT', max_length=2, choices=[(b'YT', b'YouTube'), (b'IG', b'Instagram'), (b'VN', b'Vine')])),
                ('title', models.CharField(max_length=255)),
                ('video_id', models.CharField(max_length=50)),
                ('thumbnail_url', models.CharField(max_length=255)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
    ]
