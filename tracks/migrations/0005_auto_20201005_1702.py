# Generated by Django 3.1.2 on 2020-10-05 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0004_auto_20201005_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='rank',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]