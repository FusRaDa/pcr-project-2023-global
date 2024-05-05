# Generated by Django 4.2.6 on 2024-05-05 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0058_control_threshold_control_threshold_diff'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='sample',
            constraint=models.UniqueConstraint(fields=('user', 'lab_id_num', 'sample_id'), name='unique_sample', violation_error_message='Each sample must have a unique sample ID.'),
        ),
    ]
