# Generated by Django 4.2.6 on 2023-12-17 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_kit_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='kit',
            new_name='kits',
        ),
    ]
