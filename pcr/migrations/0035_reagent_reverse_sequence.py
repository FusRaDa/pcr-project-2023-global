# Generated by Django 4.2.6 on 2024-01-29 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0034_rename_sequence_reagent_forward_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='reagent',
            name='reverse_sequence',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
