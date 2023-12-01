# Generated by Django 4.2.6 on 2023-11-28 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0012_remove_reagent_is_pcr_water_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reagent',
            name='unit_concentration',
            field=models.CharField(blank=True, choices=[('M', 'M'), ('mM', 'mM'), ('µM', 'µM'), ('nM', 'nM'), ('U/µL', 'U/µL'), ('X', 'X')], default='mM', max_length=25, null=True),
        ),
    ]