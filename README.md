<h2>To add your own Spotify Credentials:</h2>
  
- Clone the repo locally using this command: *git clone https://github.com/DeepThePatel/spotify-analytics.git*
- Create a *.env* file in the root folder
- Copy this into the file: 
```
    SPOTIPY_CLIENT_ID=
    SPOTIPY_CLIENT_SECRET=
    SPOTIPY_REDIRECT_URI=http://127.0.0.1:8000/callback
```
- Go to: https://developer.spotify.com/dashboard
- Create an app
- Copy the client id and secret from the 'Basic information' tab into the .env file

<h2>To open the duckdb shell:</h2>

```
  duckdb data/spotify.duckdb
```

<h2>To install requirements.txt libraries:</h2>

```
  pip install -r requirements.txt 
```
