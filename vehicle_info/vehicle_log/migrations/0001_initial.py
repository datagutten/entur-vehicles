# Generated by Django 2.1.4 on 2019-07-28 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_ref', models.CharField(max_length=200)),
                ('block_ref', models.CharField(max_length=200)),
                ('vehicle_ref', models.CharField(max_length=20)),
                ('item_id', models.CharField(max_length=200)),
                ('origin_quay_ref', models.CharField(max_length=20)),
                ('origin_departure_time', models.DateTimeField()),
            ],
        ),
    ]
