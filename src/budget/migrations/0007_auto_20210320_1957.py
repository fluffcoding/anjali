# Generated by Django 3.1.7 on 2021-03-20 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0006_auto_20210320_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='budget_yearly',
            field=models.IntegerField(default=600000),
        ),
    ]