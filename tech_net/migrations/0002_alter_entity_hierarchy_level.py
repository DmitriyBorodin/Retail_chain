# Generated by Django 5.1.4 on 2024-12-30 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tech_net", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entity",
            name="hierarchy_level",
            field=models.IntegerField(
                default=0, editable=False, verbose_name="Уровень иерархии"
            ),
        ),
    ]
