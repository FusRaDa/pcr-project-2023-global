# Generated by Django 4.2.6 on 2023-12-21 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_brand_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=models.ImageField(blank=True, default='brands/default-brand.png', null=True, upload_to='brands'),
        ),
        migrations.AlterField(
            model_name='kit',
            name='image',
            field=models.ImageField(blank=True, default='kits/default-kit.png', null=True, upload_to='kits'),
        ),
    ]
