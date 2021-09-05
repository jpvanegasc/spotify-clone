# Spotify API clone
## Build
This project uses Docker, so in order to set up the API (assuming you have docker installed) the only command needed is

```bash
docker-compose up -d --build
```

This sets up a postrgesql database on port 5432, and starts the api on port 8000. Given that it's built using FastAPI, if you wish to use the GUI you can go to [localhost:8000/docs](http://localhost:8000/docs)

__Important:__ make sure to have the .env file with system variables in the root of the project!

## Database Loading
In order to pre-load the DB with information, you can download and run the scripts in the folder "load_db". With "download_data.py" you can connect to Spotify's api and download full catalogues from any artist, as well as downloading information on your user profile and your created playlists.

__Important:__ make sure to have the (second) .env file inside the load_db folder! In it you have to store the Spotify api access token, which you can obtain from various ways from Spotify. I personally used the method provided on [this](https://github.com/spotify/web-api-auth-examples) repo. Also, make sure to grant enough scopes to the token!

Using the "load_db.py" script you can upload the data you downloaded to the database. Make sure you have already started the Docker container!

## Project Overview