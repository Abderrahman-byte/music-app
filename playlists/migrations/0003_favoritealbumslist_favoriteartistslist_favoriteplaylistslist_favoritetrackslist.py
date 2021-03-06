# Generated by Django 3.1.2 on 2020-10-25 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201017_1637'),
        ('tracks', '0001_initial'),
        ('playlists', '0002_auto_20201025_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteTracksList',
            fields=[
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.account')),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('tracks', models.ManyToManyField(to='tracks.Track')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FavoritePlaylistsList',
            fields=[
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.account')),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('playlist', models.ManyToManyField(to='playlists.TracksPlaylist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FavoriteArtistsList',
            fields=[
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.account')),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('artists', models.ManyToManyField(to='tracks.Artist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FavoriteAlbumsList',
            fields=[
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.account')),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('albums', models.ManyToManyField(to='tracks.Album')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
