from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys



TRACK_INFO_DIV_CLASS = "tlToogleData"

MEDIA_LINKS_DIV_CLASS = "addMedia"

SPOTIFY_LINK_ICON_CLASS = "fa-spotify"

SPOTIFY_LINK_AVAILABLE_CLASS = "mediaAction"

# TODO: Make robust in that track name is not accessed as the first meta tag
# TODO: Get the spotify link for songs that have the spotify link
def getTracklist(trackListURL):
    # Initalize parser and read HTML
    site= trackListURL
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page,'html.parser')

    trackList = []
    trackAvailable = []
    finalTrackList = []
    # Get all the track info rows in the table
    trackTable = soup.find_all(class_=TRACK_INFO_DIV_CLASS)

    # Iterate through the table and get all the track names
    for track in trackTable:
        # Check if track has been identified. This deals with IDs
        if (track.has_attr('itemprop')):
            # Get the first meta node under the main div
            trackName = track.find_next("meta")
            # Track name and artist is in the content of that meta tag
            trackList.append(trackName['content'])
            # Find the first instance of a spotify link under the track's main div
            spotifyLink = track.find_next(class_=SPOTIFY_LINK_ICON_CLASS)
            # If the spotify link node contains the SPOTIFY_LINK_AVAILABLE_CLASS then there is a spotify track linked on the site
            trackAvailable.append(SPOTIFY_LINK_AVAILABLE_CLASS in spotifyLink['class'])

    # Check to make sure the tracklist and trackAvailable arrays are smae length - this is likely never false now
    # TODO: delete lol
    if (len(trackList) != len(trackAvailable)):
        print("Length mismatch between track names and track availability")
        print("tracklist:",len(trackList),"trackAvailable:"len(trackAvailable))
        sys.exit()
    # Trims the tracklist of tracks that do not have a spotify link
    for i in range(0,len(trackList)):
        if(trackAvailable[i]):
            finalTrackList.append(trackList[i])
    return finalTrackList
