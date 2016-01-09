# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hotel_name', models.CharField(max_length=100)),
                ('item', models.CharField(max_length=100)),
                ('rating', models.IntegerField()),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('category', models.CharField(max_length=100)),
                ('veg', models.BooleanField()),
            ],
        ),
    ]
