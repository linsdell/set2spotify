import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

scope = 'user-library-read'

if len(sys.argv)>1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print(track['name'] + ' - ' + track['artists'][0]['name'])
else:
    print("Can't get token for", username)

# sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# results = sp.search(q='weezer',limit=20)

# for idx, track in enumerate(results['tracks']['items']):
#     print(idx,track['name'])
