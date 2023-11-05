# Generated by Django 4.2.6 on 2023-11-04 23:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('type', models.CharField(choices=[('DNA', 'DNA'), ('RNA', 'RNA')], default='DNA', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='AssayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('assays', models.ManyToManyField(to='pcr.assay')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('number_of_samples', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('lab_id', models.CharField(max_length=5)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('assay_list', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pcr.assaylist')),
            ],
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('lot_number', models.CharField(max_length=25)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reagent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('lot_number', models.CharField(max_length=25)),
                ('catalog_number', models.CharField(max_length=25)),
                ('storage_location', models.CharField(max_length=25)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('volume', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('unit_volume', models.CharField(choices=[('LITER', 'L'), ('MILLILITER', 'mL'), ('MICROLITER', 'µL')], default='MICROLITER', max_length=25)),
                ('stock_concentration', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('unit_concentration', models.CharField(blank=True, choices=[('NOT_APPLICABLE', 'NOT_APPLICABLE'), ('MOLES', 'M'), ('MILLIMOLES', 'mM'), ('MICROMOLES', 'µM'), ('NANOMOLES', 'nM'), ('UNITS', 'U/µL'), ('X', 'X')], default='MILLIMOLES', max_length=25, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_id_num', models.CharField(max_length=10)),
                ('sample_id', models.CharField(blank=True, max_length=25)),
                ('assay_name', models.CharField(blank=True, max_length=25)),
                ('assays', models.ManyToManyField(to='pcr.assay')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.batch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ThermalCyclerProtocol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('denature_temp', models.DecimalField(decimal_places=2, max_digits=12)),
                ('denature_duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('anneal_temp', models.DecimalField(decimal_places=2, max_digits=12)),
                ('anneal_duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('extension_temp', models.DecimalField(decimal_places=2, max_digits=12)),
                ('extension_duration', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('number_of_cycles', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SampleList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('samples', models.ManyToManyField(to='pcr.sample')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReagentOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('assay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.assay')),
                ('reagent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.reagent')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('lot_number', models.CharField(max_length=25)),
                ('type', models.CharField(choices=[('DNA', 'DNA'), ('RNA', 'RNA')], default='DNA', max_length=25)),
                ('plate_size', models.IntegerField(choices=[('8', '8'), ('24', '24'), ('48', '48'), ('96', '96'), ('384', '384'), ('<django.db.models.fields.IntegerField>', 'Custom')], default='96')),
                ('protocol', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pcr.thermalcyclerprotocol')),
                ('samples', models.ManyToManyField(to='pcr.samplelist')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flourescence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExtractionProtocol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('type', models.CharField(choices=[('DNA', 'DNA'), ('RNA', 'RNA'), ('TOTAL_NUCLEIC', 'Total Nucleic')], default='DNA', max_length=25)),
                ('reagents', models.ManyToManyField(to='pcr.reagent')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ControlOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('assay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.assay')),
                ('control', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.control')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='batch',
            name='extraction_protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pcr.extractionprotocol'),
        ),
        migrations.AddField(
            model_name='batch',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assay',
            name='controls',
            field=models.ManyToManyField(through='pcr.ControlOrder', to='pcr.control'),
        ),
        migrations.AddField(
            model_name='assay',
            name='fluorescence',
            field=models.ManyToManyField(to='pcr.flourescence'),
        ),
        migrations.AddField(
            model_name='assay',
            name='reagents',
            field=models.ManyToManyField(through='pcr.ReagentOrder', to='pcr.reagent'),
        ),
        migrations.AddField(
            model_name='assay',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='thermalcyclerprotocol',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='thermal_cycler_protocol_unique', violation_error_message='A protocol with this name already exists.'),
        ),
        migrations.AddConstraint(
            model_name='sample',
            constraint=models.UniqueConstraint(fields=('user', 'lab_id_num'), name='sample_unique', violation_error_message='A batch with this lab ID already exists.'),
        ),
        migrations.AddConstraint(
            model_name='reagent',
            constraint=models.UniqueConstraint(fields=('user', 'lot_number', 'catalog_number'), name='reagent_unique', violation_error_message='A reagent with the same lot and catalog number already exists.'),
        ),
        migrations.AddConstraint(
            model_name='flourescence',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='flourescence_unique', violation_error_message='Flourescense with this name already exists.'),
        ),
        migrations.AddConstraint(
            model_name='extractionprotocol',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='extraction_protocol_unique', violation_error_message='An extraction protocol with this name already exists.'),
        ),
        migrations.AddConstraint(
            model_name='control',
            constraint=models.UniqueConstraint(fields=('user', 'lot_number'), name='control_unique', violation_error_message='A control with this lot number already exists.'),
        ),
        migrations.AddConstraint(
            model_name='batch',
            constraint=models.UniqueConstraint(fields=('user', 'lab_id'), name='batch_unique', violation_error_message='A batch with this lab ID already exists.'),
        ),
        migrations.AddConstraint(
            model_name='assaylist',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='assay_list_unique', violation_error_message='An assay list/group with this name already exists.'),
        ),
        migrations.AddConstraint(
            model_name='assay',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='assay_unique', violation_error_message='An assay with this name already exists.'),
        ),
    ]
