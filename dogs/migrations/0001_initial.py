# Generated by Django 5.0.14 on 2025-04-12 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.CharField(max_length=800, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Breed',
                'verbose_name_plural': 'Breeds',
            },
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Dog name')),
                ('img', models.ImageField(blank=True, null=True, upload_to='dogs/', verbose_name='Image')),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dogs.breed', verbose_name='Dog Breed')),
            ],
            options={
                'verbose_name': 'Dog',
                'verbose_name_plural': 'Dogs',
            },
        ),
    ]
