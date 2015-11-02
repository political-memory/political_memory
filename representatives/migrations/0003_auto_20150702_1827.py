# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0002_fixtures'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('city', models.CharField(default=b'', max_length=255, blank=True)),
                ('street', models.CharField(default=b'', max_length=255, blank=True)),
                ('number', models.CharField(default=b'', max_length=255, blank=True)),
                ('postcode', models.CharField(default=b'', max_length=255, blank=True)),
                ('floor', models.CharField(default=b'', max_length=255, blank=True)),
                ('office_number', models.CharField(default=b'', max_length=255, blank=True)),
                ('kind', models.CharField(default=b'', max_length=255, blank=True)),
                ('name', models.CharField(default=b'', max_length=255, blank=True)),
                ('location', models.CharField(default=b'', max_length=255, blank=True)),
                ('country', models.ForeignKey(to='representatives.Country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('fingerprint', models.CharField(unique=True, max_length=40)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('kind', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('fingerprint', models.CharField(unique=True, max_length=40)),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(default=b'', max_length=10, blank=True)),
                ('kind', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mandate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('fingerprint', models.CharField(unique=True, max_length=40)),
                ('role', models.CharField(default=b'', help_text=b'Eg.: president of a political group at the European Parliament', max_length=25, blank=True)),
                ('begin_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('link', models.URLField()),
                ('constituency', models.ForeignKey(related_name='mandates', to='representatives.Constituency', null=True)),
                ('group', models.ForeignKey(related_name='mandates', to='representatives.Group', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(default=b'', max_length=255, blank=True)),
                ('kind', models.CharField(default=b'', max_length=255, blank=True)),
                ('address', models.ForeignKey(related_name='phones', to='representatives.Address', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('fingerprint', models.CharField(unique=True, max_length=40)),
                ('slug', models.SlugField(max_length=100)),
                ('remote_id', models.CharField(unique=True, max_length=255)),
                ('first_name', models.CharField(default=b'', max_length=255, blank=True)),
                ('last_name', models.CharField(default=b'', max_length=255, blank=True)),
                ('full_name', models.CharField(max_length=255)),
                ('gender', models.SmallIntegerField(default=0, choices=[(0, b'N/A'), (1, b'F'), (2, b'M')])),
                ('birth_place', models.CharField(default=b'', max_length=255, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('cv', models.TextField(default=b'', blank=True)),
                ('photo', models.CharField(max_length=512, null=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WebSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(default=b'', max_length=2048, blank=True)),
                ('kind', models.CharField(default=b'', max_length=255, blank=True)),
                ('representative', models.ForeignKey(to='representatives.Representative')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='phone',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
        ),
        migrations.AddField(
            model_name='mandate',
            name='representative',
            field=models.ForeignKey(related_name='mandates', to='representatives.Representative'),
        ),
        migrations.AddField(
            model_name='email',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
        ),
        migrations.AddField(
            model_name='address',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
        ),
    ]
