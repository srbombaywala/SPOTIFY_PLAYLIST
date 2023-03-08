import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup

# GET THE DATE FOR THE TOP 100 SONG FROM BILLBOARD WEBSITE #
user_date = input("Which year do you want to travel to ?\nType the date in this format\nYYYY-MM-DD: ")
year = user_date.split("-")[0]
billboard_url = f"https://www.billboard.com/charts/hot-100/{user_date}"

# GET THE RESPONSE FROM THE BILLBOARD WEBSITE #
response = requests.get(url= billboard_url)
data = response.text

# USE BEAUTIFULSOUP AND GENERATE A LIST OF 100 SONG TITLE - U NEED TO INSPECT THE WEBSITE TO FIND THE NAME,ID AND CLASS #
soup = BeautifulSoup(data, 'html.parser')
song_list = [song.getText().strip() for song in soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")]

# BILLBOARD WORK ENDS #
# GO TO SPOTIFY WEBSITE AND IN DEVELOPERS, CREATE A NEW APP AND GET YOUR CLIENT ID AND CLENT SECRET #

Client_ID = "UR CLIENT ID"
Client_Secret = "UR CLIENT SECRET"
redirect_Uri = "https://www.example.com/callback/"
user_scope = "playlist-modify-private"

# AUTHENTICATE TO SPOTIFY USING SPOTIPY AND OBTAIN YOUR TOKEN AND USER ID #
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
                    scope=user_scope,
                    redirect_uri=redirect_Uri,
                    client_id=Client_ID,
                    client_secret=Client_Secret,
                    show_dialog=True,
                    cache_path="token.txt"
                    ))

user_id = sp.current_user()["id"]
# U MUST RUN THE ABOVE CODE WHICH WILL INVOKE A WEBPAGE ON REDIRECT_URI PROVIDED WHERE U NEED TO AGREE AND COPY THE 
# ADDRESS URL FROM THE BROWSER AND PASTE IN THE TERMINAL TO AUTHENTICATE AND GENERATE TOKEN.TXT.
# JUST RUN, THEN ON BROWSER PRESS AGREE, COPY THE URL OF THE NEXT PAGE, PASTE IN THE TERMINAL.
# THE ABOVE LINE NEEDS TO BE DONE ONLY FOR THE FIRST TIME (WHEN TOKEN.TXT IS NOT GENERATED).

# FIND THE URI FOR ALL THE SONG OBTAINED ABOVE BY SEARCHING #
song_uri = []
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        song_uri.append(result["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"{song} doesn't exists in spotify. Skipped")

# CREATE A NEW PLAYIST#
playlist_ID = sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100",public=False,collaborative=False,description="1998 top 100")

# ADD SONGS TO THE NEWLY CREATED PLAYLIST #
sp.playlist_add_items(playlist_id=playlist_ID["id"], items=song_uri)

# OPEN SPOTIFY.COM AND YOU WILL FIND YOUR PLAYLIST THERE #
# PUT ON THE HEADSET AND ENJOY !!!!! #
