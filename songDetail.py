import requests
import json
from requests.exceptions import HTTPError
from headers import shazam_api_headers, audioDB_api_headers

# Urls for the endpoints
shazam_search_url = "https://shazam.p.rapidapi.com/search"
shazam_get_details_url = "https://shazam.p.rapidapi.com/songs/get-details"
audioDB_search_track_url = "https://theaudiodb.p.rapidapi.com/searchtrack.php"

# Song class with attributes or song details
# Methods that allow us to set the song details though API calls


class Song:

    # Attributes that come from Shazam
    artist, albumImage = '', ''
    album, label = '', ''
    released_date, genre = '', ''
    youtubelink, lyrics = '', ''
    song_key, track = '', ''
    thumbnail = ''

    # Attributes that come from AudioDB
    description, mood = '', ''

    # JSON data attributes
    shazam_search_json_data = ''
    shazam_get_details_json_data = ''
    audioDB_get_details_json_data = ''

    # Class constructor, song and query are used in the 1st API call
    def __init__(self, song, shazamSearchQuery):
        self.song = song
        self.shazamSearchQuery = shazamSearchQuery

    # Sets all of our class attributes, song details
    def set_all_attributes(self):
        try:
            # Shazam Search Query: Get Artist, Album Image, and Song Key
            self.shazam_search_json_data = self.get_info_from_api(
                shazam_search_url, shazam_api_headers, self.shazamSearchQuery)
            shazam_search = self.shazam_search_json_data["tracks"]["hits"][0]["track"]

            # Accesing values from python list, and assigning them to class attributes
            self.track = shazam_search["title"]
            self.artist = shazam_search["subtitle"]
            self.albumImage = shazam_search["share"]["image"]
            self.song_key = shazam_search["key"]

            # Shazam getDetails Query: Track, Album, Label, Released Date, Lyrics...
            details_query = {"key": self.song_key, "locale": "en-US"}
            self.shazam_get_details_json_data = self.get_info_from_api(
                shazam_get_details_url, shazam_api_headers, details_query)
            get_details_metadata = self.shazam_get_details_json_data["sections"][0]["metadata"]

            # Accesing values from python list, and assigning them to class attributes
            self.album = get_details_metadata[0]["text"]
            self.label = get_details_metadata[1]["text"]
            self.released_date = get_details_metadata[2]["text"]
            self.youtubelink = self.shazam_get_details_json_data[
                "sections"][2]["youtubeurl"]["actions"][0]["uri"]
            self.thumbnail = self.shazam_get_details_json_data[
                "sections"][2]["youtubeurl"]["image"]["url"]
            self.genre = self.shazam_get_details_json_data["genres"]["primary"]

            # Using formatted lyrics method to clean up lyrics
            self.lyrics = self.formatted_lyrics(
                self.shazam_get_details_json_data["sections"][1]["text"])

        except Exception as err:
            return f'Error: {err}, occured in Shazam Query'

        # Set data attributes from AudioDB
        audioDB_api_query = {"s": self.artist, "t": self.song}
        self.audioDB_get_details_json_data = self.get_info_from_api(
            audioDB_search_track_url, audioDB_api_headers, audioDB_api_query)
        self.description = self.get_audioDB_json_string(
            "Description", "strDescriptionEN")
        self.mood = self.get_audioDB_json_string("Mood", "strMood")

    # Used to query api
    def get_info_from_api(self, url, header, query):
        try:
            response = requests.request(
                "GET", url, headers=header, params=query)
            response.raise_for_status()
            # json.loads returns a python list...
            json_data = json.loads(response.text)
            return json_data
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    # Used to format data from audioDB and...
    # ...error handling when detail not found in AudioDB
    def get_audioDB_json_string(self, attr, DBstr):
        try:
            str = self.audioDB_get_details_json_data["track"][0][DBstr]
            return str
        except Exception as err:
            return 'Cant find ' + attr

    # Formats lyrics data into more user readable
    def formatted_lyrics(self, lyrics_list):
        formatted = ''
        for line in lyrics_list:
            formatted = formatted + line + '\n'
        return formatted
