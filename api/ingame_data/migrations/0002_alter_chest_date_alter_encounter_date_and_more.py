# Generated by Django 4.1 on 2023-03-04 15:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingame_data", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chest",
            name="date",
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name="encounter",
            name="date",
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name="roll",
            name="date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
