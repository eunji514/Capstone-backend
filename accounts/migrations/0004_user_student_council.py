# Generated by Django 5.2 on 2025-06-01 16:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_emailverification'),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='student_council',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='schedule.studentcouncil'),
        ),
    ]
