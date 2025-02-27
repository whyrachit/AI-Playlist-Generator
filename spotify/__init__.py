# This file makes the spotify folder a Python package.
# You can also import functions from auth and playlist here if needed.
from .auth import spotify_authenticate
from .playlist import create_spotify_playlist, add_tracks_to_playlist
