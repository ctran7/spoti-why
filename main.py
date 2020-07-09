import spotify_functions
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep

CACHE = ".cache-" + "test"
scope = "playlist-modify-public, user-read-playback-state,user-modify-playback-state, user-library-modify"
client_credentials_manager=SpotifyOAuth(scope=scope)
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, cache_path=CACHE))

user_id = sp.me()['id']
playlist_name = "temp"


#allows multiple songs to repeat by creating a temporary playlist that will be deleted
#once exit out of tab/browser
playlist_id, playlist_uri = spotify_functions.create_playlist(sp, user_id, playlist_name)
song_uris = []
song_uris.append(spotify_functions.search_item(sp, 'track', 'Dal Shabet Someone Like U'))
spotify_functions.add_songs_to_temp_playlist(sp,user_id, playlist_id, song_uris)
sp.start_playback(context_uri = playlist_uri)
sleep(10)
spotify_functions.delete_playlist_stop_playing(sp, user_id, playlist_id)


#adding all of an album's tracks to your liked songs
album_uri = spotify_functions.search_item(sp, 'album', 'Hwasa Maria')
spotify_functions.add_all_album_to_liked(sp, album_uri)
