# Generated by Django 4.0.6 on 2022-07-28 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournamentprize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize', models.TextField(max_length=80)),
            ],
        ),
    ]
