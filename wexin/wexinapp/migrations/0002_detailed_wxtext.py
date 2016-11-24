# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-19 13:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wexinapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detailed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SurfaceName', models.CharField(max_length=30, null=True)),
                ('Img', models.ImageField(blank=True, null=True, upload_to='img')),
                ('Introduce', models.TextField(null=True)),
                ('Price', models.FloatField(null=True)),
                ('ProId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wexinapp.Product')),
            ],
        ),
        migrations.CreateModel(
            name='WxText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='img')),
                ('text', models.TextField(null=True)),
            ],
        ),
    ]