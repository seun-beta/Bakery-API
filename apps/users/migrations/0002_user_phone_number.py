# Generated by Django 4.1.1 on 2022-10-01 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]