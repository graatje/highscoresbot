# Generated by Django 4.0.6 on 2022-07-29 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingame_data', '0003_roll'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playername', models.TextField(max_length=50)),
                ('location', models.TextField(max_length=80)),
                ('date', models.DateField()),
            ],
        ),
    ]