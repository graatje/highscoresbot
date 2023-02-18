# Generated by Django 4.1 on 2023-02-18 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ingame_data", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DefaultClanname",
            fields=[
                (
                    "guild",
                    models.PositiveBigIntegerField(primary_key=True, serialize=False),
                ),
                ("clan", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="HighscoreConfig",
            fields=[
                ("highscorename", models.TextField(primary_key=True, serialize=False)),
                ("url", models.URLField()),
                ("pagesamount", models.PositiveSmallIntegerField()),
                ("fieldmapping", models.JSONField()),
                ("verbose_name", models.TextField(default="")),
                ("intfields", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="WorldbossHighscore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("player", models.TextField()),
                ("damage", models.PositiveIntegerField()),
                ("rank", models.PositiveSmallIntegerField()),
                (
                    "worldboss",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="ingame_data.worldboss",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Highscore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rank", models.IntegerField()),
                ("data", models.JSONField()),
                (
                    "highscore",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="highscores.highscoreconfig",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="highscore",
            constraint=models.UniqueConstraint(
                fields=("rank", "highscore"), name="unique_highscoreranks"
            ),
        ),
    ]
