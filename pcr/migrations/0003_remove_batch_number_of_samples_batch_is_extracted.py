# Generated by Django 4.2.6 on 2023-12-11 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch',
            name='number_of_samples',
        ),
        migrations.AddField(
            model_name='batch',
            name='is_extracted',
            field=models.BooleanField(default=False),
        ),
    ]
