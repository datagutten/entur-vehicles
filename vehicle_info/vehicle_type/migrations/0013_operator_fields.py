# Generated by Django 3.1.5 on 2021-05-15 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle_type', '0012_vehicle_null_fields'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operator',
            options={'ordering': ['display_name', 'name', 'vehicle_prefix']},
        ),
        migrations.AddField(
            model_name='operator',
            name='display_name',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='operator',
            name='vehicle_prefix',
            field=models.IntegerField(unique=True),
        ),
    ]
