# Generated by Django 4.2.6 on 2024-01-24 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0021_alter_reagent_volume'),
    ]

    operations = [
        migrations.AddField(
            model_name='plate',
            name='type',
            field=models.CharField(choices=[('PCR', 'PCR'), ('qPCR', 'qPCR')], default='PCR', max_length=25),
        ),
    ]
