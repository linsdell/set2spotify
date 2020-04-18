from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import sys

site= "https://www.1001tracklists.com/tracklist/1klq0dvt/elif-the-anjunadeep-edition-299-2020-04-16.html"
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page,'html.parser')

TRACK_INFO_DIV_CLASS = "tlToogleData"

MEDIA_LINKS_DIV_CLASS = "addMedia"

SPOTIFY_LINK_ICON_CLASS = "fa-spotify"

trackList = []
trackAvailable = []

# Get all the track info rows in the table
trackTable = soup.find_all(class_=TRACK_INFO_DIV_CLASS)
# TODO: Make robust in that track name is not accessed as the first meta tag
# Iterate through the table and get all the track names
for track in trackTable:
    trackName = track.find_next("meta")
    trackList.append(trackName['content'])

# Get all the media link rows in the table
linksTable = soup.find_all(class_=MEDIA_LINKS_DIV_CLASS)
# Print binary condition for the track having a spotify link
for link in linksTable:
    spotifyLink = link.find_next(class_=SPOTIFY_LINK_ICON_CLASS)
    trackAvailable.append(MEDIA_LINKS_DIV_CLASS in spotifyLink['class'])

if (len(trackList) != len(trackAvailable)):
    print("Length mismatch between track names and track availability")
    sys.exit()


for i in range(0,len(trackList)):
    print(trackList[i],trackAvailable[i])
