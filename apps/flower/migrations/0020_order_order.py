# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flower', '0019_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order',
            field=models.CharField(default=None, max_length=10000),
        ),
    ]
