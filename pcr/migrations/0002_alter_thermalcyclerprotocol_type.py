# Generated by Django 4.2.6 on 2023-12-25 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thermalcyclerprotocol',
            name='type',
            field=models.CharField(choices=[('DNA', 'DNA'), ('RNA', 'RNA')], default='DNA', max_length=100),
        ),
    ]
