# Generated by Django 4.2.6 on 2023-11-08 19:13

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
                ('method', models.CharField(choices=[('qPCR', 'qPCR'), ('PCR', 'PCR')], default='qPCR', max_length=25)),
                ('type', models.CharField(choices=[('DNA', 'DNA'), ('RNA', 'RNA')], default='DNA', max_length=25)),
                ('sample_volume', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('reaction_volume', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='AssayCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('assays', models.ManyToManyField(to='pcr.assay')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('number_of_samples', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('lab_id', models.CharField(max_length=5)),
                ('date_performed', models.DateTimeField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('assay_list', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pcr.assaycode')),
            ],
        ),
        migrations.CreateModel(
            name='ExtractionProtocol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('type', models.CharField(choices=[('DNA', 'DNA'), ('RNA', 'RNA'), ('TOTAL_NUCLEIC', 'Total Nucleic')], default='DNA', max_length=25)),
                ('doc_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Plate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('brand', models.CharField(blank=True, max_length=25)),
                ('lot_number', models.CharField(max_length=25)),
                ('catalog_number', models.CharField(max_length=25)),
                ('size', models.IntegerField(choices=[('8', '8'), ('24', '24'), ('48', '48'), ('96', '96'), ('384', '384'), ('<django.db.models.fields.IntegerField>', 'Custom')], default='96')),
                ('amount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('location', models.ManyToManyField(to='pcr.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_performed', models.DateTimeField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('plate', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pcr.plate')),
            ],
        ),
        migrations.CreateModel(
            name='Reagent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('brand', models.CharField(blank=True, max_length=25)),
                ('lot_number', models.CharField(max_length=25)),
                ('catalog_number', models.CharField(max_length=25)),
                ('is_pcr_water', models.BooleanField(default=False)),
                ('usage', models.CharField(choices=[('EXTRACTION', 'EXTRACTION'), ('PCR', 'PCR'), ('GENERAL', 'GENERAL')], default='GENERAL', max_length=25)),
                ('volume', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('unit_volume', models.CharField(choices=[('LITER', 'L'), ('MILLILITER', 'mL'), ('MICROLITER', 'µL')], default='MICROLITER', max_length=25)),
                ('stock_concentration', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('unit_concentration', models.CharField(blank=True, choices=[('NOT_APPLICABLE', 'NOT_APPLICABLE'), ('MOLES', 'M'), ('MILLIMOLES', 'mM'), ('MICROMOLES', 'µM'), ('NANOMOLES', 'nM'), ('UNITS', 'U/µL'), ('X', 'X')], default='MILLIMOLES', max_length=25, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('location', models.ManyToManyField(to='pcr.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tube',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('brand', models.CharField(blank=True, max_length=25)),
                ('lot_number', models.CharField(max_length=25)),
                ('catalog_number', models.CharField(max_length=25)),
                ('amount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('location', models.ManyToManyField(to='pcr.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TubeExtraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('amount_per_sample', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('protocol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.extractionprotocol')),
                ('tube', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.tube')),
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReagentExtraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('amount_per_sample', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('protocol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.extractionprotocol')),
                ('reagent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.reagent')),
            ],
        ),
        migrations.CreateModel(
            name='ReagentAssay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_concentration', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('final_concentration_unit', models.CharField(choices=[('NOT_APPLICABLE', 'NOT_APPLICABLE'), ('MOLES', 'M'), ('MILLIMOLES', 'mM'), ('MICROMOLES', 'µM'), ('NANOMOLES', 'nM'), ('UNITS', 'U/µL'), ('X', 'X')], default='MICROMOLES', max_length=25)),
                ('order', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('assay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.assay')),
                ('reagent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.reagent')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessPlate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('DNA', 'DNA'), ('RNA', 'RNA')], default='DNA', max_length=25)),
                ('plate', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pcr.plate')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcr.process')),
                ('protocol', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pcr.thermalcyclerprotocol')),
                ('samples', models.ManyToManyField(to='pcr.sample')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='process',
            name='protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pcr.thermalcyclerprotocol'),
        ),
        migrations.AddField(
            model_name='process',
            name='samples',
            field=models.ManyToManyField(to='pcr.sample'),
        ),
        migrations.AddField(
            model_name='process',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Flourescence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='extractionprotocol',
            name='reagents',
            field=models.ManyToManyField(through='pcr.ReagentExtraction', to='pcr.reagent'),
        ),
        migrations.AddField(
            model_name='extractionprotocol',
            name='tubes',
            field=models.ManyToManyField(through='pcr.TubeExtraction', to='pcr.tube'),
        ),
        migrations.AddField(
            model_name='extractionprotocol',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('lot_number', models.CharField(max_length=25)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assay',
            name='controls',
            field=models.ManyToManyField(to='pcr.control'),
        ),
        migrations.AddField(
            model_name='assay',
            name='fluorescence',
            field=models.ManyToManyField(to='pcr.flourescence'),
        ),
        migrations.AddField(
            model_name='assay',
            name='reagents',
            field=models.ManyToManyField(through='pcr.ReagentAssay', to='pcr.reagent'),
        ),
        migrations.AddField(
            model_name='assay',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='tube',
            constraint=models.UniqueConstraint(fields=('user', 'lot_number', 'catalog_number'), name='tube_unique', violation_error_message='Tubes with the same lot and catalog number already exists.'),
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
            constraint=models.UniqueConstraint(fields=('user', 'lot_number', 'catalog_number'), name='reagent_unique', violation_error_message='Reagents with the same lot and catalog number already exists.'),
        ),
        migrations.AddConstraint(
            model_name='plate',
            constraint=models.UniqueConstraint(fields=('user', 'lot_number', 'catalog_number'), name='plate_unique', violation_error_message='Tubes with the same lot and catalog number already exists.'),
        ),
        migrations.AddConstraint(
            model_name='location',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='location_unique', violation_error_message='A location with the same name already exists.'),
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
            model_name='batch',
            constraint=models.UniqueConstraint(fields=('user', 'lab_id'), name='batch_unique', violation_error_message='A batch with this lab ID already exists.'),
        ),
        migrations.AddConstraint(
            model_name='assaycode',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='assay_list_unique', violation_error_message='An assay list/group with this name already exists.'),
        ),
        migrations.AddConstraint(
            model_name='assay',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='assay_unique', violation_error_message='An assay with this name already exists.'),
        ),
    ]
