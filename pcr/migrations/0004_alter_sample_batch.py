# Generated by Django 4.2.6 on 2023-11-19 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0003_alter_extractionprotocol_doc_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batch_fk', to='pcr.batch'),
        ),
    ]