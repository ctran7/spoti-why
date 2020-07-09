# shows artist info for a URN or URL

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
import atexit
import signal

'''
 create temp playlist
 add songs to playlist
 set to repeat - just play the playlist
 delete temp playlist
'''
CACHE = ".cache-" + "test"
scope = "playlist-modify-public, user-read-playback-state,user-modify-playback-state, user-library-modify"
client_credentials_manager=SpotifyOAuth(scope=scope)
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, cache_path=CACHE))

user_id = sp.me()['id']
playlist_name = "temp"
playlist_id = None
playlist_uri = None

def delete_playlist_stop_playing():
    #stops playing songs
    sp.current_user_saved_tracks_add(tracks=None)
    #deletes playlist
    sp.user_playlist_unfollow(user_id, playlist_id)

def search_item(type_str, search_str):
    search_dict = {}
    result = sp.search(search_str, limit=10, type=type_str)
    search_res = result[type_str + "s"]['items']
    for i in range(len(search_res)):
        print(search_res[i]['name'])
        search_dict[search_res[i]['name']] = search_res[i]['uri']
    #pprint.pprint(result['tracks']['items'][0]['name'])
    print("Have you found searched item you were looking for?")
    answer = input()
    if answer.lower() == "yes":
        print("Please type your selected item")
        item = input()
        uri = search_dict[item]
        print(uri)
        return uri

def add_all_album_to_liked(album_uri):
    album_ret = sp.album_tracks(album_uri)
    uris = [i['uri'] for i in album_ret['items']]
    sp.current_user_saved_tracks_add(tracks=uris)

def add_songs_to_temp_playlist(user_id, playlist_name):
    global playlist_id, playlist_uri
    new_playlist = sp.user_playlist_create(user_id, playlist_name)
    playlist_id, playlist_uri = new_playlist['id'], new_playlist['uri']
    sp.user_playlist_add_tracks(user_id, playlist_id, ['spotify:track:3CYH422oy1cZNoo0GTG1TK'])
    #start playing the newly created playlist
    sp.start_playback(context_uri = playlist_uri)
