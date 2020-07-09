# shows artist info for a URN or URL

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def delete_playlist_stop_playing(sp, user_id, playlist_id):
    #stops playing songs
    sp.pause_playback()
    #deletes playlist
    sp.user_playlist_unfollow(user_id, playlist_id)

def search_item(sp, type_str, search_str):
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

def add_all_album_to_liked(sp, album_uri):
    album_ret = sp.album_tracks(album_uri)
    uris = [i['uri'] for i in album_ret['items']]
    sp.current_user_saved_tracks_add(tracks=uris)

#creates playlist and returns id/uri for the given playlist
def create_playlist(sp, user_id, playlist_name):
    new_playlist = sp.user_playlist_create(user_id, playlist_name)
    playlist_id, playlist_uri = new_playlist['id'], new_playlist['uri']
    return (playlist_id, playlist_uri)

def add_songs_to_temp_playlist(sp,user_id, playlist_id, uris):
    sp.user_playlist_add_tracks(user_id, playlist_id, uris)
    #start playing the newly created playlist
    #sp.start_playback(context_uri = playlist_uri)
