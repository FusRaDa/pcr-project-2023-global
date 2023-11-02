# Generated by Django 4.2.6 on 2023-11-02 16:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assay',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=25, unique=True)),
                ('type', models.CharField(choices=[('DNA', 'DNA'), ('RNA', 'RNA')], default='DNA', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='AssayList',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=25, unique=True)),
                ('number_of_samples', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('lab_id', models.CharField(max_length=5, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=25, unique=True)),
                ('lot_number', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='ControlOrder',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('order', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='ExtractionProtocol',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=25, unique=True)),
                ('type', models.CharField(choices=[('DNA', 'DNA'), ('RNA', 'RNA'), ('TOTAL_NUCLEIC', 'Total Nucleic')], default='DNA', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Flourescence',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plate',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=25)),
                ('lot_number', models.CharField(max_length=25)),
                ('type', models.CharField(choices=[('DNA', 'DNA'), ('RNA', 'RNA')], default='DNA', max_length=25)),
                ('plate_size', models.IntegerField(choices=[('8', '8'), ('24', '24'), ('48', '48'), ('96', '96'), ('384', '384'), ('<django.db.models.fields.IntegerField>', 'Custom')], default='96')),
            ],
        ),
        migrations.CreateModel(
            name='Reagent',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=25)),
                ('lot_number', models.CharField(max_length=25)),
                ('catalog_number', models.CharField(max_length=25)),
                ('storage_location', models.CharField(max_length=25)),
                ('volume', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('unit_volume', models.CharField(choices=[('LITER', 'L'), ('MILLILITER', 'mL'), ('MICROLITER', 'µL')], default='MICROLITER', max_length=25)),
                ('stock_concentration', models.DecimalField(blank=True, decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('unit_concentration', models.CharField(blank=True, choices=[('NOT_APPLICABLE', 'NOT_APPLICABLE'), ('MOLES', 'M'), ('MILLIMOLES', 'mM'), ('MICROMOLES', 'µM'), ('NANOMOLES', 'nM'), ('UNITS', 'U/µL'), ('X', 'X')], default='MILLIMOLES', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('lab_id_num', models.CharField(max_length=10, unique=True)),
                ('sample_id', models.CharField(max_length=25)),
                ('assay', models.ManyToManyField(to='pcr.assay')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.batch')),
            ],
        ),
        migrations.CreateModel(
            name='ThermalCyclerProtocol',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=25)),
                ('denature_temp', models.DecimalField(decimal_places=2, max_digits=12)),
                ('denature_duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('anneal_temp', models.DecimalField(decimal_places=2, max_digits=12)),
                ('anneal_duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('extension_temp', models.DecimalField(decimal_places=2, max_digits=12)),
                ('extension_duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('number_of_cycles', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='SampleList',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=25)),
                ('samples', models.ManyToManyField(to='pcr.sample')),
            ],
        ),
        migrations.CreateModel(
            name='ReagentOrder',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('order', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('assay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.assay')),
                ('reagent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.reagent')),
            ],
        ),
        migrations.AddConstraint(
            model_name='reagent',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('lot_number'), django.db.models.functions.text.Lower('catalog_number'), name='lot_catalog_number_unique', violation_error_message='A reagent with the same lot and catalog number already exists.'),
        ),
        migrations.AddField(
            model_name='plate',
            name='protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pcr.thermalcyclerprotocol'),
        ),
        migrations.AddField(
            model_name='plate',
            name='samples',
            field=models.ManyToManyField(to='pcr.samplelist'),
        ),
        migrations.AddField(
            model_name='extractionprotocol',
            name='reagents',
            field=models.ManyToManyField(to='pcr.reagent'),
        ),
        migrations.AddField(
            model_name='controlorder',
            name='assay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.assay'),
        ),
        migrations.AddField(
            model_name='controlorder',
            name='control',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.control'),
        ),
        migrations.AddField(
            model_name='batch',
            name='assay_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pcr.assaylist'),
        ),
        migrations.AddField(
            model_name='batch',
            name='extraction_protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pcr.extractionprotocol'),
        ),
        migrations.AddField(
            model_name='assaylist',
            name='assays',
            field=models.ManyToManyField(to='pcr.assay'),
        ),
        migrations.AddField(
            model_name='assay',
            name='fluorescence',
            field=models.ManyToManyField(to='pcr.flourescence'),
        ),
    ]
