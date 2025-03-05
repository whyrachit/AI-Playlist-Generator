import re
import time
import concurrent.futures
from spotipy.exceptions import SpotifyException
import difflib  # For fuzzy matching

def create_spotify_playlist(sp, playlist_name: str, description: str):
    """
    Creates a new playlist in the authenticated user's Spotify account.
    """
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name, public=False, description=description)
    return playlist['id']

def is_valid_spotify_id(spotify_id: str) -> bool:
    """
    Checks if the given spotify_id is a valid Spotify track ID.
    Spotify track IDs are typically 22 characters in base62.
    """
    return bool(re.fullmatch(r'[0-9A-Za-z]{22}', spotify_id))

def playlist_add_items_with_retry(sp, playlist_id, track_uris, max_retries=3):
    """
    Attempts to add track URIs to a playlist with retry logic.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            sp.playlist_add_items(playlist_id, track_uris)
            return
        except SpotifyException as e:
            if e.http_status in [429, 502]:
                retry_after = e.headers.get("Retry-After", None)
                wait_time = int(retry_after) if retry_after and retry_after.isdigit() else 5
                time.sleep(wait_time * (attempt + 1))  # Exponential backoff.
                attempt += 1
            else:
                raise e
    raise Exception("Max retries reached for adding tracks to playlist.")

def find_track_uri(song: dict, sp):
    """
    Searches for a Spotify track URI based on the song's title and artist.
    Uses an exact match first, and falls back to a looser query if necessary.
    """
    song_name = song.get('name', '').strip()
    artist_name = song.get('artist', '').strip()
    query = f'track:"{song_name}" artist:"{artist_name}"'
    try:
        result = sp.search(q=query, type='track', limit=1)
        tracks = result.get('tracks', {}).get('items', [])
        if not tracks:
            # Fallback to a broader search.
            query = f"{song_name} {artist_name}"
            result = sp.search(q=query, type='track', limit=10)
            tracks = result.get('tracks', {}).get('items', [])
            # Use fuzzy matching to pick the best candidate based on artist similarity.
            if tracks:
                best_match = None
                highest_ratio = 0
                for t in tracks:
                    candidate_artists = ", ".join([artist["name"].lower() for artist in t["artists"]])
                    ratio = difflib.SequenceMatcher(None, artist_name.lower(), candidate_artists).ratio()
                    if ratio > highest_ratio:
                        highest_ratio = ratio
                        best_match = t
                tracks = [best_match] if best_match else []
        if tracks:
            track_uri = tracks[0]['uri']
            if track_uri.startswith("spotify:track:"):
                return track_uri
    except Exception as ex:
        print(f"Error finding track URI for '{song_name}' by '{artist_name}': {ex}")
    return None

def add_tracks_to_playlist(sp, playlist_id: str, song_recommendations: list):
    """
    Searches for tracks on Spotify based on the song recommendations and adds them to the playlist.
    Uses parallelization for improved performance.
    """
    track_uris = []
    songs_to_search = []
    
    # Since the agent will not supply Spotify IDs now, always search for the track.
    for song in song_recommendations:
        # If a spotify_id is provided and is valid, use it; otherwise, search using the API.
        spotify_id = song.get('spotify_id', '').strip()
        if spotify_id and is_valid_spotify_id(spotify_id):
            track_uri = f"spotify:track:{spotify_id}"
            track_uris.append(track_uri)
        else:
            songs_to_search.append(song)
    
    if songs_to_search:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_song = {executor.submit(find_track_uri, song, sp): song for song in songs_to_search}
            for future in concurrent.futures.as_completed(future_to_song):
                track_uri = future.result()
                if track_uri:
                    track_uris.append(track_uri)
    
    if track_uris:
        playlist_add_items_with_retry(sp, playlist_id, track_uris)
