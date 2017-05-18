# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientDataModel',
            fields=[
                ('patient_id', models.IntegerField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('doctor_id', models.IntegerField()),
                ('birthday', models.DateField(default=datetime.date)),
                ('patient_email', models.EmailField(default=b'', max_length=254)),
            ],
        ),
        migrations.DeleteModel(
            name='PatientModel',
        ),
    ]
