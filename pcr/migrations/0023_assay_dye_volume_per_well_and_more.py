# Generated by Django 4.2.6 on 2024-01-25 01:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pcr', '0022_plate_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='assay',
            name='dye_volume_per_well',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='assay',
            name='ladder_volume_per_gel',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.CreateModel(
            name='Dye',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('brand', models.CharField(blank=True, max_length=25)),
                ('lot_number', models.CharField(max_length=25)),
                ('catalog_number', models.CharField(max_length=25)),
                ('amount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('exp_date', models.DateField(blank=True, default=None, null=True)),
                ('location', models.ManyToManyField(to='pcr.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='assay',
            name='dye',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='pcr.dye'),
        ),
    ]
