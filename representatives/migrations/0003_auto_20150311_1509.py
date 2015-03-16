# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0002_representative_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(max_length=10, null=True, blank=True)),
                ('kind', models.CharField(max_length=255, null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='mandate',
            name='kind',
        ),
        migrations.RemoveField(
            model_name='mandate',
            name='name',
        ),
        migrations.RemoveField(
            model_name='mandate',
            name='short_id',
        ),
        migrations.AddField(
            model_name='mandate',
            name='group',
            field=models.ForeignKey(to='representatives.Group', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='representative',
            name='active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='mandate',
            name='constituency'
        ),
        migrations.AddField(
            model_name='mandate',
            name='constituency',
            field=models.ForeignKey(to='representatives.Constituency', null=True),
            preserve_default=True,
        ),
    ]
