import sys
import spotipy
import spotipy.util as util
import tracklistScraper, spotifyComponent


scope = 'playlist-modify-public'
username = 'jlinsdell'

# TEST playlist ID
playlist_id = '2dl4t2rD4lQ3PjpKKa27im'

set_url = "https://www.1001tracklists.com/tracklist/pn9j9ck/luttrell-the-anjunadeep-edition-287-2020-01-16.html"

token = util.prompt_for_user_token(username,scope)

tracklist = tracklistScraper.getTracklist(set_url)

trackIDs = spotifyComponent.getTrackIDsFromTracklist(token,tracklist)

spotifyComponent.addTracksToPlaylistID(token,username,playlist_id,trackIDs)
