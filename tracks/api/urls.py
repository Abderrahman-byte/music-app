from django.urls import path

from . import views

urlpatterns = [
    path('tracks/top', views.TopTracks, name='top-tracks'),
    path('track/<str:id>', views.TrackApiView, name='track-details'),
    path('album/<str:id>', views.AlbumApiView, name='album-details'),
    path('artist/<str:id>', views.ArtistApiView, name='artist-details'),
]