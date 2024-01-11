# Generated by Django 4.2.6 on 2024-01-11 14:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pcr', '0010_rename_min_samples_process_min_samples_per_gel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ladder',
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
    ]
