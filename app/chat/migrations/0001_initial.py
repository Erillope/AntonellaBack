# Generated by Django 5.1.6 on 2025-06-22 01:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0004_remove_employeeaccounttabledata_dni_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatTable',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.useraccounttabledata')),
            ],
            options={
                'db_table': 'chat',
            },
        ),
        migrations.CreateModel(
            name='ChatMessageTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('message_type', models.CharField(max_length=10)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.useraccounttabledata')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chattable')),
            ],
            options={
                'db_table': 'chat_message',
                'ordering': ['timestamp'],
            },
        ),
    ]
