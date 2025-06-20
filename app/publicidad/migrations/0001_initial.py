# Generated by Django 5.1.6 on 2025-06-17 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('store_service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicidadTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_date', models.DateField()),
            ],
            options={
                'db_table': 'publicidad',
            },
        ),
        migrations.CreateModel(
            name='PublicidadImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField()),
                ('publicidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='publicidad.publicidadtable')),
            ],
            options={
                'db_table': 'publicidad_image',
            },
        ),
        migrations.CreateModel(
            name='ProductPublicidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.producttabledata')),
                ('publicidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_items', to='publicidad.publicidadtable')),
            ],
            options={
                'db_table': 'product_publicidad',
            },
        ),
        migrations.CreateModel(
            name='ServicePublicidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('publicidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_items', to='publicidad.publicidadtable')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_service.storeservicetabledata')),
            ],
            options={
                'db_table': 'service_publicidad',
            },
        ),
    ]
