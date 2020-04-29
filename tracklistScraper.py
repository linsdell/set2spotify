from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys



TRACK_INFO_DIV_CLASS = "tlToogleData"

MEDIA_LINKS_DIV_CLASS = "addMedia"

SPOTIFY_LINK_ICON_CLASS = "fa-spotify"

SPOTIFY_LINK_AVAILABLE_CLASS = "mediaAction"

# TODO: Make robust in that track name is not accessed as the first meta tag
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
            trackName = track.find_next("meta")
            trackList.append(trackName['content'])
            print(trackName['content'])

    # Get all the media link rows in the table
    linksTable = soup.find_all(class_=MEDIA_LINKS_DIV_CLASS)
    # Print binary condition for the track having a spotify link
    for link in linksTable:
        spotifyLink = link.find_next(class_=SPOTIFY_LINK_ICON_CLASS)
        trackAvailable.append(SPOTIFY_LINK_AVAILABLE_CLASS in spotifyLink['class'])

    if (len(trackList) != len(trackAvailable)):
        print("Length mismatch between track names and track availability")
        print(len(trackList),len(trackAvailable))
        # for i in range(0, min(len(trackList),len(trackAvailable))):
        #     print(trackList[i])
        sys.exit()
    for i in range(0,len(trackList)):
        if(trackAvailable[i]):
            finalTrackList.append(trackList[i])
    return finalTrackList
