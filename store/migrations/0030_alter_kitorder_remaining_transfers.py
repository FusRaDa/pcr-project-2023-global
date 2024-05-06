# Generated by Django 4.2.6 on 2024-04-24 19:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_storereagent_forward_sequence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitorder',
            name='remaining_transfers',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]