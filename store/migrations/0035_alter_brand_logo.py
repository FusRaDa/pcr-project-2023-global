# Generated by Django 4.2.6 on 2024-05-12 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_alter_brand_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=models.ImageField(blank=True, default='default-brand.png', null=True, upload_to='brands'),
        ),
    ]
