# Generated by Django 4.2.6 on 2024-01-10 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0004_process_min_samples'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gel',
            name='wells',
        ),
        migrations.AddField(
            model_name='gel',
            name='size',
            field=models.IntegerField(choices=[(8, '8'), (12, '12'), (24, '24'), (48, '48')], default=24),
        ),
    ]