# Generated by Django 4.2.6 on 2024-01-13 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0014_process_pcr_dna_json_process_pcr_rna_json_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
