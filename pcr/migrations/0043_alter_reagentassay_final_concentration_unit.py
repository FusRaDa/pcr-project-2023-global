# Generated by Django 4.2.6 on 2024-02-20 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0042_alter_reagentassay_final_concentration_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reagentassay',
            name='final_concentration_unit',
            field=models.CharField(blank=True, default=None, max_length=25, null=True),
        ),
    ]