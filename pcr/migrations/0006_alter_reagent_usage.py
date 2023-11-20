# Generated by Django 4.2.6 on 2023-11-20 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0005_alter_sample_batch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reagent',
            name='usage',
            field=models.CharField(choices=[('EXTRACTION', 'EXTRACTION'), ('PCR', 'PCR')], default='PCR', max_length=25),
        ),
    ]
