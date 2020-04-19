import sys
import spotipy
import spotipy.util as util

scope = 'playlist-read-private'
username = 'jlinsdell'

token = util.prompt_for_user_token(username,scope)

def getAllPlaylistNames(authToken):
    sp = spotipy.Spotify(auth=authToken)
    allPlaylistNames = []
    stillMorePlaylists = True
    currentOffset = 0;
    while stillMorePlaylists:
        newPlaylists = sp.current_user_playlists(limit=50,offset = 50*currentOffset)
        currentOffset += 1
        if(len(newPlaylists['items'])<50):
            stillMorePlaylists = False
        for playlist in newPlaylists['items']:
            allPlaylistNames.append(playlist['name'])
    return allPlaylistNames


if token:
    result = getAllPlaylistNames(token)
    for name in result:
        print(name)
