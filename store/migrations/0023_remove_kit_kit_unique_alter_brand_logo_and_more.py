# Generated by Django 4.2.6 on 2024-04-24 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_alter_brand_logo_alter_kit_image'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='kit',
            name='kit_unique',
        ),
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='brands'),
        ),
        migrations.AlterField(
            model_name='kit',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='kits'),
        ),
    ]