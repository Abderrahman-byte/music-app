# Generated by Django 3.1.2 on 2020-10-17 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201017_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]