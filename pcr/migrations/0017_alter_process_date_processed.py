# Generated by Django 4.2.6 on 2024-01-14 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0016_process_batches'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='date_processed',
            field=models.DateField(blank=True, default=None, editable=False, null=True),
        ),
    ]