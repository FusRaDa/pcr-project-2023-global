# Generated by Django 4.2.6 on 2024-01-30 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0035_reagent_reverse_sequence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='lab_id',
            field=models.CharField(max_length=3),
        ),
    ]
