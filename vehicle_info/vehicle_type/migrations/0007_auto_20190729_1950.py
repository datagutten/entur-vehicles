# Generated by Django 2.1.4 on 2019-07-29 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_type', '0006_auto_20190729_1944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='operator_name',
        ),
        migrations.AlterField(
            model_name='expectedvehicle',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_type.Vehicle'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='operator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='vehicle_type.Operator', verbose_name='Operatør'),
        ),
    ]
