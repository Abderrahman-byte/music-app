# Generated by Django 3.1.2 on 2020-10-26 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0005_tracksplaylist_is_public'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favoriteplaylistslist',
            old_name='playlist',
            new_name='playlists',
        ),
    ]
