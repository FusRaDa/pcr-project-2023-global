# Generated by Django 4.2.6 on 2024-01-29 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0033_assay_multiplicates'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reagent',
            old_name='sequence',
            new_name='forward_sequence',
        ),
    ]
