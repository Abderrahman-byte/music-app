# Generated by Django 3.1.2 on 2020-10-05 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0003_track_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]