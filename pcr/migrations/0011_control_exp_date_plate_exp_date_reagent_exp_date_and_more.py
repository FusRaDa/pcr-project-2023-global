# Generated by Django 4.2.6 on 2023-11-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0010_rename_flourescence_fluorescence'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='exp_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='plate',
            name='exp_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='reagent',
            name='exp_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='tube',
            name='exp_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]