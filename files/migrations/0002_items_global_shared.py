# Generated by Django 4.2.3 on 2023-07-13 09:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("files", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="items",
            name="global_shared",
            field=models.BooleanField(default=False),
        ),
    ]