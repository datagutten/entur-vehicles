# Generated by Django 2.1.4 on 2019-07-29 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_type', '0002_auto_20190728_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectedvehicle',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle_type.Vehicle'),
        ),
    ]
