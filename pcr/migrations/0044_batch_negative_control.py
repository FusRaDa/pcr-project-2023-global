# Generated by Django 4.2.6 on 2024-02-23 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0043_alter_reagentassay_final_concentration_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='negative_control',
            field=models.BooleanField(default=True),
        ),
    ]
