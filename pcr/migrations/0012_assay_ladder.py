# Generated by Django 4.2.6 on 2024-01-11 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0011_ladder'),
    ]

    operations = [
        migrations.AddField(
            model_name='assay',
            name='ladder',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='pcr.ladder'),
        ),
    ]
