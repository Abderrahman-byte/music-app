from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.db import utils

from .serializers import (
    PlaylistSimpleSerializer, 
    PlaylistDetailedSerializer, 
    FavoriteTracksSerializer,
    FavoriteArtistsSerializer,
    FavoriteAlbumsSerializer,
    FavoritePlaylistsSerializer
)
from .permissions import IsAuthorReadOnlyIfPublic
from ..models import TracksPlaylist, Follow
from tracks.models import Track, Artist, Album
from tracks.api.serializers import ArtistSimpleSerializer


class UserPlaylists(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request) :
        user = request.user
        user_playlists = user.tracksplaylist_set.all()
        user_playlists_count = user.tracksplaylist_set.count()

        PlaylistsData = PlaylistDetailedSerializer(user_playlists, many=True) if 'details' in request.query_params else PlaylistSimpleSerializer(user_playlists, many=True) 
        context = {
            'data': PlaylistsData.data,
            'count': user_playlists_count 
        }

        return Response(context, status=200, content_type='application/json')
    
    def post(self, request) :
        data = request.data
        validated_data = {
            'user': request.user,
            'title': data.get('title'),
            'is_public': data.get('is_public', True),
            'description': data.get('description'),
        }

        if validated_data.get('title') is None :
            return Response({'detail': 'Playlist title field is required.'}, status=400, content_type='application/json')

        try :
            pl = PlaylistSimpleSerializer().create(**validated_data)
            context = PlaylistSimpleSerializer(pl).data
            return Response(context, status=201, content_type='application/json')
        except Exception as ex :
            return Response({'detail': ex.__str__()}, status=400, content_type='application/json')


class PlaylistDetails(APIView) :
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthorReadOnlyIfPublic]
    
    def get(self, request, id) :
        try :
            pl = TracksPlaylist.objects.get(pk=id)
        except TracksPlaylist.DoesNotExist :
            return Response({'detail': f'Playlist with id {id} doesnt exist'}, status=404, content_type='application/json')
        
        self.check_object_permissions(request, pl)
        context = PlaylistDetailedSerializer(pl).data
        return Response(context, status=200, content_type='application/json')

    def put(self, request, id) :
        try :
            pl = TracksPlaylist.objects.get(pk=id)
        except TracksPlaylist.DoesNotExist :
            return Response({'detail': f'Playlist with id {id} doesnt exist'}, status=404, content_type='application/json')
        
        self.check_object_permissions(request, pl)
        try :
            data = request.data
            pl = PlaylistSimpleSerializer().update(pl, **data)
            context = PlaylistDetailedSerializer(pl).data
            return Response(context, status=201, content_type='application/json')
        except Exception as ex :
            return Response({'detail': ex.__str__()}, content_type='application/json', status=400)

    def post(self, request, id) :
        try :
            pl = TracksPlaylist.objects.get(pk=id)
        except TracksPlaylist.DoesNotExist :
            return Response({'detail': f'Playlist with id {id} doesnt exist'}, status=404, content_type='application/json')
        
        self.check_object_permissions(request, pl)
        data = request.data
        action = data.get('action', True)
        tracks_ids = data.get('tracks_ids')

        if tracks_ids is None :
            return Response({'detail': 'tracks_ids field is required.'}, status=400, content_type='application/json')
        elif type(tracks_ids) == str :
            tracks_ids = [tracks_ids]
        elif type(tracks_ids) != list :
            return Response({'detail': 'tracks_ids field type unsupported'}, status=400, content_type='application/json')

        try :
            tracks_list = [Track.objects.get(pk=track_id) for track_id in tracks_ids]
        except Track.DoesNotExist :
            return Response({'detail': f'A Track in tracks list doesnt exist'}, status=400, content_type='application/json')

        if action is None :
            return Response({'detail': 'action field is required.'}, status=400, content_type='application/json')
        
        elif action == True:
            pl.tracks.add(*tracks_list)
            pl.save()
            return Response(status=204, content_type='application/json')
        
        elif action == False:
            pl.tracks.remove(*tracks_list)
            pl.save()
            return Response(status=204, content_type='application/json')
        
        else :
            return Response({'detail': f'Action doesnt exist'}, status=400, content_type='application/json')

    def delete(self, request, id) :
        try :
            pl = TracksPlaylist.objects.get(pk=id)
        except TracksPlaylist.DoesNotExist :
            return Response({'detail': f'Playlist with id {id} doesnt exist'}, status=404, content_type='application/json')
        
        self.check_object_permissions(request, pl)
        pl.delete()
        return Response(status=204)


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def ListSubscriptions(request) :
    data = request.query_params
    user = request.user
    limit = 25
    index = 0

    try :
        limit = int(data.get('limit', 25))
    except :
        limit = 25

    try :
        index = int(data.get('index', 0))
    except :
        index = 0

    subscriptions = user.follow_set.all()
    following = [sub.artist for sub in subscriptions][index: index + limit]
    context = {
        'artists': ArtistSimpleSerializer(following, many=True).data, 
        'subscriptions_count': subscriptions.count()
    }
    return Response(context, content_type='application/json')


class Subscription(APIView) :
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id) :
        try :
            artist = Artist.objects.get(pk=id)
        except Artist.DoesNotExist :
            return Response({'detail': 'Artist Doesnt exist.'}, status=404, content_type='application/json')

        user = request.user
        try :
            Follow.objects.get(user=user, artist=artist)
            return Response(status=204)
        except Follow.DoesNotExist :
            return Response({'detail': 'User is not following this artist'}, status=404, content_type='application/json')

    def post(self, request, id) :
        try :
            artist = Artist.objects.get(pk=id)
        except Artist.DoesNotExist :
            return Response({'detail': 'Artist Doesnt exist.'}, status=404, content_type='application/json')

        user = request.user
        try :
            artist.follow_set.create(user=user)
            artist.save()
            return Response(status=204)
        except utils.IntegrityError :
            return Response({'detail': 'User already following artist'}, status=400, content_type='application/json')

    def delete(self, request, id) :
        try :
            artist = Artist.objects.get(pk=id)
        except Artist.DoesNotExist :
            return Response({'detail': 'Artist Doesnt exist.'}, status=404, content_type='application/json')

        user = request.user
        
        try:
            subscription = Follow.objects.get(user=user, artist=artist)
            subscription.delete()
            return Response(status=204)
        except Follow.DoesNotExist :
            return Response({'detail': 'User cannot unfollow artist.'}, status=404, content_type='application/json')


class FavoriteTracksAPI(APIView) :
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request) :
        user = request.user
        fav_tracks = user.favoritetrackslist
        context = FavoriteTracksSerializer(fav_tracks).data
        return Response(context, status=200, content_type='application/json')
    
    def post(self, request) :
        data = request.data
        track_id = data.get('id')
        user = request.user
        fav_tracks = user.favoritetrackslist

        if track_id is None :
            return Response({'detail': 'id of track is required'}, status=400, content_type='application/json')

        try :
            track = Track.objects.get(pk=track_id)
            fav_tracks.tracks.add(track)
            return Response(status=204)
        except Track.DoesNotExist :
            return Response({'details': f'track with id {track_id} doesnt exist.'}, status=404, content_type='application/json')
    
    def delete(self, request) :
        data = request.data
        track_id = data.get('id')
        user = request.user
        fav_tracks = user.favoritetrackslist

        if track_id is None :
            return Response({'detail': 'id of track is required'}, status=400, content_type='application/json')

        try :
            track = Track.objects.get(pk=track_id)
            fav_tracks.tracks.remove(track)
            return Response(status=204)
        except Track.DoesNotExist :
            return Response({'details': f'track with id {track_id} doesnt exist.'}, status=404, content_type='application/json')
    

class FavoriteArtistsAPI(APIView) :
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request) :
        user = request.user
        fav_artists = user.favoriteartistslist
        context = FavoriteArtistsSerializer(fav_artists).data
        return Response(context, status=200, content_type='application/json')
    
    def post(self, request) :
        data = request.data
        artist_id = data.get('id')
        user = request.user
        fav_artists = user.favoriteartistslist

        if artist_id is None :
            return Response({'detail': 'id of artist is required'}, status=400, content_type='application/json')

        try :
            artist = Artist.objects.get(pk=artist_id)
            fav_artists.artists.add(artist)
            return Response(status=204)
        except Artist.DoesNotExist :
            return Response({'details': f'artist with id {track_id} doesnt exist.'}, status=404, content_type='application/json')
    
    def delete(self, request) :
        data = request.data
        artist_id = data.get('id')
        user = request.user
        fav_artists = user.favoriteartistslist

        if artist_id is None :
            return Response({'detail': 'id of artist is required'}, status=400, content_type='application/json')

        try :
            artist = Artist.objects.get(pk=artist_id)
            fav_artists.artists.remove(artist)
            return Response(status=204)
        except Artist.DoesNotExist :
            return Response({'details': f'artist with id {track_id} doesnt exist.'}, status=404, content_type='application/json')
    

class FavoriteAlbumsAPI(APIView) :
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request) :
        user = request.user
        fav_albums = user.favoritealbumslist
        context = FavoriteAlbumsSerializer(fav_albums).data
        return Response(context, status=200, content_type='application/json')

    def post(self, request) :
        data = request.data
        album_id = data.get('id')
        user = request.user
        fav_albums = user.favoritealbumslist

        if album_id is None :
            return Response({'detail': 'id of albums is required'}, status=400, content_type='application/json')

        try :
            album = Album.objects.get(pk=album_id)
            fav_albums.albums.add(album)
            return Response(status=204)
        except Album.DoesNotExist :
            return Response({'details': f'album with id {track_id} doesnt exist.'}, status=404, content_type='application/json')
    
    def delete(self, request) :
        data = request.data
        album_id = data.get('id')
        user = request.user
        fav_albums = user.favoritealbumslist

        if album_id is None :
            return Response({'detail': 'id of album is required'}, status=400, content_type='application/json')

        try :
            album = Album.objects.get(pk=album_id)
            fav_albums.albums.remove(album)
            return Response(status=204)
        except Album.DoesNotExist :
            return Response({'details': f'album with id {track_id} doesnt exist.'}, status=404, content_type='application/json')
    

class FavoritePlaylistsAPI(APIView) :
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request) :
        user = request.user
        fav_playlists = user.favoriteplaylistslist
        context = FavoritePlaylistsSerializer(fav_playlists).data
        return Response(context, status=200, content_type='application/json')

    def post(self, request) :
        data = request.data
        playlist_id = data.get('id')
        user = request.user
        fav_playlists = user.favoriteplaylistslist

        if playlist_id is None :
            return Response({'detail': 'id of playlist is required'}, status=400, content_type='application/json')

        try :
            playlist = TracksPlaylist.objects.get(pk=playlist_id)
            fav_playlists.playlists.add(playlist)
            return Response(status=204)
        except TracksPlaylist.DoesNotExist :
            return Response({'details': f'playlist with id {track_id} doesnt exist.'}, status=404, content_type='application/json')
    
    def delete(self, request) :
        data = request.data
        playlist_id = data.get('id')
        user = request.user
        fav_playlists = user.favoriteplaylistslist

        if playlist_id is None :
            return Response({'detail': 'id of playlist is required'}, status=400, content_type='application/json')

        try :
            playlist = TracksPlaylist.objects.get(pk=playlist_id)
            fav_playlists.playlists.remove(playlist)
            return Response(status=204)
        except TracksPlaylist.DoesNotExist :
            return Response({'details': f'playlist with id {track_id} doesnt exist.'}, status=404, content_type='application/json')
    