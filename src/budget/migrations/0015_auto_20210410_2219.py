# Generated by Django 3.1.7 on 2021-04-10 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0014_auto_20210410_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='others',
            field=models.IntegerField(default=0),
        ),
    ]