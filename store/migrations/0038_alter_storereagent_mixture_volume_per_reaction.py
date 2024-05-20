# Generated by Django 4.2.6 on 2024-05-12 20:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_alter_kit_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storereagent',
            name='mixture_volume_per_reaction',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]