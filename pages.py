from flask import Flask, render_template, request
import time
import songDetail as SD

# Instance of Flask Class, argument is the name of the application
# This is needed so that Flask knows where to look for resources such as templates and static files.
app = Flask(__name__)

# getting local time to pass to base.html
seconds = time.time()
local_time = time.ctime(seconds)

# Route tells Flask what URL should trigger our function and what kinds of requests we can make
# home() function returns the HTML template we want to display in the user’s browser... 
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":

        # grabs value from base.html template form on POST
        song = request.form["sng"]

        # forms query for our API call
        shazam_api_query = {"term": song,"locale": "en-US", "offset": "0", "limit": "5"}

        # create instance of Song class and pass in query
        songDetail = SD.Song(song, shazam_api_query)

        # responsible for SPI call and assigning all class attributes
        songDetail.set_all_attributes()

        # dictionary for each of the attributes to be looped through on base.html
        song_detail_dict = {'Song Searched': songDetail.song, 'Artist': songDetail.artist,
                            'Track': songDetail.track, 'Label': songDetail.label,
                            'Released Date': songDetail.released_date, 'Album': songDetail.album,
                            'Description': songDetail.description, 'Genre': songDetail.genre,
                            'Mood': songDetail.mood, 'Lyrics': songDetail.lyrics
                            }

        # used in base.html to display details or not
        submit = True

        # used to pass values to our base.html template
        return render_template("base.html", song_detail_dict=song_detail_dict, search_date=local_time,
                               albumImg=songDetail.albumImage, youTube=songDetail.youtubelink,
                                thumbnail=songDetail.thumbnail, submit=submit, json=songDetail.shazam_get_details_json_data)

    # otherwise, just render base.html
    else:
        return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)
