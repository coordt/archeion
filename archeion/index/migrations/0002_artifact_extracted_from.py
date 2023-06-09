# Generated by Django 4.1.7 on 2023-05-07 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("index", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="artifact",
            name="extracted_from",
            field=models.ForeignKey(
                blank=True,
                help_text="The artifact used to extract this artifact.",
                limit_choices_to={"link": models.F("link")},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="extractions",
                to="index.artifact",
                verbose_name="extracted from",
            ),
        ),
    ]
