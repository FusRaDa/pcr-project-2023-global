# Generated by Django 4.2.6 on 2024-01-28 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0029_assay_dye_in_ladder'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='is_plus_one_well',
            field=models.BooleanField(default=True),
        ),
    ]
