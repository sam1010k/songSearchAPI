import requests
import json
from requests.exceptions import HTTPError
from headers import shazam_api_headers, audioDB_api_headers

shazam_api_url = "https://shazam.p.rapidapi.com/search"

audioDB_api_url = "https://theaudiodb.p.rapidapi.com/searchtrack.php"

class Song:

    json_data = ''

    # from Shazam
    artist, albumImage = '', ''

    # from AudioDB
    album, description = '', ''
    genre, mood = '', ''
    youTubeLink, track = '', ''
    lyrics = ''

    # Class constructor
    def __init__(self, song, shazamQuery):
        self.song = song
        self.shazamQuery = shazamQuery
    
    # Sets all of our class attributes, song details
    def set_all_attributes(self):

        # Set data from Shazam API
        self.json_data = self.get_info_from_api(shazam_api_url, shazam_api_headers, self.shazamQuery)
        try:
            self.artist = self.json_data["tracks"]["hits"][0]["track"]["subtitle"]
            self.albumImage = self.json_data["tracks"]["hits"][0]["track"]["share"]["image"]
        except Exception as err:
            return 'Cant find the requested song'


        # Set data from AudioDB
        audioDB_api_query = {"s": self.artist,"t": self.song}
        self.json_data = self.get_info_from_api(audioDB_api_url, audioDB_api_headers, audioDB_api_query)
        self.album = self.get_audioDB_json_string("Album", "strAlbum")
        self.description = self.get_audioDB_json_string("Description", "strDescriptionEN")
        self.genre = self.get_audioDB_json_string("Genre", "strGenre")
        self.mood = self.get_audioDB_json_string("Mood", "strMood")
        self.youTubeLink = self.get_audioDB_json_string("YouTube Link", "strMusicVid")
        self.track = self.get_audioDB_json_string("Track", "strTrack")
        self.lyrics = self.get_audioDB_json_string("Lyrics", "strTrackLyrics")
    
    # Used to query api
    def get_info_from_api(self,url,header,query):
        try:
            response = requests.request("GET", url, headers=header, params=query)
            response.raise_for_status()
            json_data = json.loads(response.text)
            return json_data
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
    
    # Error handling when detail not found in database
    def get_audioDB_json_string(self, attr, DBstr):
        try:
            str = self.json_data["track"][0][DBstr]
            return str
        except Exception as err:
            return 'Cant find ' + attr
