# Generated by Django 2.2.1 on 2019-08-24 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_type', '0010_auto_20190729_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectedvehicle',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_type.Vehicle'),
        ),
    ]
