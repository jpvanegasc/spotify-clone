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
This project consists on a basic CRUD systems for artists, albums, tracks, playlists and users. (Make sure to check the E/R database diagram on the "docs" folder!) It's based on five database tables and endpoints (artists, albums, tracks, playlists and users), on which the different REST methods are used.

The project tree is as follows:

.
└── spotify-clone

    ├── alembic # migration management

    ├── app # main module

    |   ├── crud

    |   |   ├── music.py

    |   |   └── user.py

    |   ├── models

    |   |   ├── music.py

    |   |   └── user.py

    |   ├── routers

    |   |   ├── music.py

    |   |   └── user.py

    |   ├── schemas

    |   |   ├── music.py

    |   |   └── user.py

    |   ├── config.py

    |   ├── database.py

    |   └── main.py

    ├── docs # useful docs

    |   └── 'spotify clone db e-r.pdf'

    ├── load_db # down and upload spotify data

    |   ├── files

    |   |   ├── albums.json

    |   |   ├── artists.json

    |   |   ├── playlists.json

    |   |   ├── tracks.json

    |   |   └── user.json

    |   ├── .env

    |   ├── download_data.py

    |   └── load_db.py

    ├── .env

    ├── .gitignore

    ├── alembic.ini

    ├── docker-compose.yml

    ├── Pipfile

    ├── Pipfile.lock

    └── README.md


As mentioned before, this project was built using Docker (bonus no. 1).

Some new functionalities that I was thinking but couldn't implement (because time ran out):

* Search of user by email
* Get all of a given user playlists'
* Create a special playlist table on which the user's favorite songs are stored, and its corresponding endpoint
