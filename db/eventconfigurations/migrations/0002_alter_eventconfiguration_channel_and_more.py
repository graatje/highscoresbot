# Generated by Django 4.0.6 on 2022-07-28 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventconfigurations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventconfiguration',
            name='channel',
            field=models.PositiveBigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='eventconfiguration',
            name='pingrole',
            field=models.PositiveBigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='eventconfiguration',
            name='time_in_channel',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddConstraint(
            model_name='eventconfiguration',
            constraint=models.UniqueConstraint(fields=('guild', 'eventname'), name='unique_events'),
        ),
    ]