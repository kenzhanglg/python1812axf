# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-03-12 12:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_order_ordergoods'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='number',
            new_name='identifier',
        ),
    ]