# Generated by Django 4.2.6 on 2024-01-28 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0031_reagent_sequence_alter_assay_dye_in_ladder_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reagent',
            name='pcr_reagent',
            field=models.CharField(blank=True, choices=[('GENERAL', 'General'), ('PRIMER', 'Primer'), ('POLYMERASE', 'Polymerase'), ('WATER', 'Water')], default=None, max_length=25, null=True),
        ),
    ]
