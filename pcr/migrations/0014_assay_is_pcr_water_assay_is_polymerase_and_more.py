# Generated by Django 4.2.6 on 2023-11-29 14:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0013_alter_reagent_unit_concentration'),
    ]

    operations = [
        migrations.AddField(
            model_name='assay',
            name='is_pcr_water',
            field=models.CharField(choices=[('TRUE', 'TRUE'), ('FALSE', 'FALSE')], default='FALSE', max_length=25),
        ),
        migrations.AddField(
            model_name='assay',
            name='is_polymerase',
            field=models.CharField(choices=[('TRUE', 'TRUE'), ('FALSE', 'FALSE')], default='FALSE', max_length=25),
        ),
        migrations.AlterField(
            model_name='reagent',
            name='stock_concentration',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='reagent',
            name='unit_concentration',
            field=models.CharField(blank=True, choices=[('M', 'M'), ('mM', 'mM'), ('µM', 'µM'), ('nM', 'nM'), ('U/µL', 'U/µL'), ('X', 'X')], default=None, max_length=25, null=True),
        ),
    ]