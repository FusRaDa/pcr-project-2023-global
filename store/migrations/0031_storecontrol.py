# Generated by Django 4.2.6 on 2024-04-29 21:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_alter_kitorder_remaining_transfers'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('kit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.kit')),
            ],
        ),
    ]
