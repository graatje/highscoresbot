# Generated by Django 4.0.6 on 2022-07-28 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
        ('eventconfigurations', '0002_alter_eventconfiguration_channel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventconfiguration',
            name='eventname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='config.eventname'),
        ),
    ]
