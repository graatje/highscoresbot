# Generated by Django 4.0.6 on 2022-07-29 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingame_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='encounter',
            name='level',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
