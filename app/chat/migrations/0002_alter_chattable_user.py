# Generated by Django 5.1.6 on 2025-06-22 01:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        ('user', '0004_remove_employeeaccounttabledata_dni_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chattable',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.useraccounttabledata', unique=True),
        ),
    ]
