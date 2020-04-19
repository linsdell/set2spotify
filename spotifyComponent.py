import sys
import spotipy
import spotipy.util as util

QUERY_SPACE_PLACEHOLDER = " "
QUERY_TYPE_TRACK = "&type=track"
QUERY_FILTER_ARTIST = "artist:"
QUERY_FILTER_TRACK = "track:"


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

def getAllPlaylistNamesandIDs(authToken):
    sp = spotipy.Spotify(auth=authToken)
    playlistDict = {}
    stillMorePlaylists = True
    currentOffset = 0;
    while stillMorePlaylists:
        newPlaylists = sp.current_user_playlists(limit=50,offset = 50*currentOffset)
        currentOffset += 1
        if(len(newPlaylists['items'])<50):
            stillMorePlaylists = False
        for playlist in newPlaylists['items']:
            playlistDict[playlist['name']]=playlist['id']
    return playlistDict


def trackInfoToQuery(trackInfo):
    # Full track name just as it appears in the tracklist
    trackName_Full = trackInfo.replace(" ",QUERY_SPACE_PLACEHOLDER)

    splitInfo = trackInfo.split(' - ')
    artist = splitInfo[0]
    artist = artist.replace(" & ",QUERY_SPACE_PLACEHOLDER)
    artist = artist.replace(" ft. ",QUERY_SPACE_PLACEHOLDER)
    artist = artist.replace(" ",QUERY_SPACE_PLACEHOLDER)
    trackName = splitInfo[1]
    trackName = trackName.replace(" ",QUERY_SPACE_PLACEHOLDER)

    # Full track name with no & in artist name
    trackName_noAmpersand = artist + QUERY_SPACE_PLACEHOLDER + QUERY_FILTER_TRACK + trackName

    # Only track name, no artist
    trackName_noArtist = trackName

    return {"trackName_Full":trackName_Full,"trackName_noAmpersand":trackName_noAmpersand,"trackName_noArtist":trackName_noArtist}

def callTrackQuery(authToken,query):
    sp = spotipy.Spotify(auth=authToken)
    results = sp.search(q=query,type='track')
    return results

def processQuery(queryResults):
    print("query made:",queryResults['tracks']['href'])
    print("number of tracks:",queryResults['tracks']['total'],"|","name of track:",queryResults['tracks']['items'][0]['name'],"\n")
    print("number of tracks:",queryResults['tracks']['total'])
    print("number of tracks (2):",len(queryResults['tracks']['items']))
    print("name of track:",queryResults['tracks']['items'][0]['name'])
    print("id of track:",queryResults['tracks']['items'][0]['id'])

# TODO: add second query where it removes artist name between 'ft.' and '-'
# TODO: investigate the importance of 'track:' in the query
def getTrackIDsFromTracklist(token,tracklist):
    trackIDs = []
    for track in tracklist:
        trackQuery = trackInfoToQuery(track)["trackName_noAmpersand"]
        trackQueryResults = callTrackQuery(token,trackQuery)
        if(trackQueryResults['tracks']['total']!=0):
            trackID = trackQueryResults['tracks']['items'][0]['id']
            trackIDs.append(trackID)
        else:
            print("Error finding track:", track, "\n\tUsing query:", trackQuery)
    return trackIDs

def showAllPlaylistNamesandIDs(token):
    result = getAllPlaylistNamesandIDs(token)
    for name in result:
        print(name,result[name])

def addTracksToPlaylistID(token,username,playlist_id,trackIDs):
    sp = spotipy.Spotify(auth=token)
    sp.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id,trackIDs)
    sp.user_playlist_add_tracks(username, playlist_id,trackIDs)
