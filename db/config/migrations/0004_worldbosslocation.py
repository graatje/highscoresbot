# Generated by Django 4.0.6 on 2022-07-28 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_honeylocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worldbosslocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField(max_length=80)),
            ],
        ),
    ]
