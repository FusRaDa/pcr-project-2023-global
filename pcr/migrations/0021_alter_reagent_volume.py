# Generated by Django 4.2.6 on 2024-01-22 02:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0020_process_gels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reagent',
            name='volume',
            field=models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
