# Generated by Django 4.0.6 on 2022-07-29 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingame_data', '0002_encounter_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playername', models.TextField(max_length=50)),
                ('pokemon', models.TextField(max_length=50)),
                ('date', models.DateField()),
                ('level', models.PositiveSmallIntegerField(null=True)),
            ],
        ),
    ]