# Generated by Django 3.1.7 on 2021-04-10 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0013_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='others',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]