# Generated by Django 3.2.13 on 2022-05-18 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("homework", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="submition",
            name="data",
            field=models.URLField(max_length=400, unique=True),
        ),
    ]
