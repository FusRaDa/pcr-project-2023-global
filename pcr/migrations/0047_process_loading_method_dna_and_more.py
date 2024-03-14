# Generated by Django 4.2.6 on 2024-03-12 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcr', '0046_alter_assay_name_alter_assaycode_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='loading_method_dna',
            field=models.CharField(choices=[('ORGANIZED', 'Organized'), ('COMPRESSED', 'Compressed')], default='ORGANIZED', max_length=25),
        ),
        migrations.AddField(
            model_name='process',
            name='loading_method_qdna',
            field=models.CharField(choices=[('ORGANIZED', 'Organized'), ('COMPRESSED', 'Compressed')], default='ORGANIZED', max_length=25),
        ),
        migrations.AddField(
            model_name='process',
            name='loading_method_qrna',
            field=models.CharField(choices=[('ORGANIZED', 'Organized'), ('COMPRESSED', 'Compressed')], default='ORGANIZED', max_length=25),
        ),
        migrations.AddField(
            model_name='process',
            name='loading_method_rna',
            field=models.CharField(choices=[('ORGANIZED', 'Organized'), ('COMPRESSED', 'Compressed')], default='ORGANIZED', max_length=25),
        ),
    ]
