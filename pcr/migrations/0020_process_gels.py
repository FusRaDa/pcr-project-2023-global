# Generated by Django 4.2.6 on 2024-01-20 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0019_process_plates'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='gels',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]