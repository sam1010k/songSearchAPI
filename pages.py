from flask import Flask, redirect, url_for, render_template, request
import songDetail as SD

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/song_search", methods = ["POST","GET"])
def song_search():
    if request.method=="POST":
        song = request.form["sng"]

        shazam_api_query = {"term": song,"locale":"en-US","offset":"0","limit":"5"}
        songDetail = SD.Song(song, shazam_api_query)
        songDetail.set_all_attributes()
        
        song_detail_dict = {'Song Searched':songDetail.song , 'Artist': songDetail.artist,
                            'Album':songDetail.album , 'Description': songDetail.description,
                            'Genre':songDetail.genre , 'Mood': songDetail.mood,
                            'Track':songDetail.track , 'Lyrics': songDetail.lyrics}


        submit = True
        return render_template("song_search.html", song_detail_dict=song_detail_dict,
                        albumImg = songDetail.albumImage, youTube = songDetail.youTubeLink,
                        submit=submit)
    else:
        return render_template("song_search.html")

if __name__ == "__main__":
    app.run(debug=True)