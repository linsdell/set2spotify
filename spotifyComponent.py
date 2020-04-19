import sys
import spotipy
import spotipy.util as util

QUERY_SPACE_PLACEHOLDER = "%20"

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

def trackInfoToQueries(trackInfo):
    # Full track name just as it appears in the tracklist
    trackName_Full = trackInfo.replace(" ",QUERY_SPACE_PLACEHOLDER)
    # Full track name with no & in artist name
    splitInfo = trackInfo.split(' - ')
    artist = splitInfo[0].replace(" & ",QUERY_SPACE_PLACEHOLDER)
    artist = artist.replace(" ",QUERY_SPACE_PLACEHOLDER)
    trackName = splitInfo[1].replace(" ",QUERY_SPACE_PLACEHOLDER)
    trackName_noAmpersand = artist + QUERY_SPACE_PLACEHOLDER +trackName
    # Only track name, no artist
    trackName_noArtist = trackName
    return {"trackName_Full":trackName_Full,"trackName_noAmpersand":trackName_noAmpersand,"trackName_noArtist":trackName_noArtist}

if token:
    result = getAllPlaylistNames(token)
    for name in result:
        print(name)

print(trackInfoToQueries("David Hôhme & Dustin Nantais - The Predicament (Soulfeed Remix)")["trackName_noAmpersand"])
