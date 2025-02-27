"""
playlist.py - Functions to create and manage Spotify playlists.

This module provides functions to create a new playlist in the authenticated user's Spotify account
and to add tracks to the playlist based on song recommendations.
"""

def create_spotify_playlist(sp, playlist_name: str, description: str):
    """
    Creates a new playlist in the authenticated user's Spotify account.
    
    Args:
        sp (spotipy.Spotify): An authenticated Spotipy client instance.
        playlist_name (str): The name for the new playlist.
        description (str): A description for the new playlist.
        
    Returns:
        str: The Spotify playlist ID of the newly created playlist.
    """
    # Get the current user's ID
    user_id = sp.current_user()['id']
    
    # Create a new (private) playlist
    playlist = sp.user_playlist_create(user_id, playlist_name, public=False, description=description)
    return playlist['id']

def add_tracks_to_playlist(sp, playlist_id: str, song_recommendations: list):
    """
    Searches for tracks on Spotify based on the song recommendations and adds them to the playlist.
    
    Each song recommendation should be a dictionary with at least 'name' and 'artist' keys.
    
    Args:
        sp (spotipy.Spotify): An authenticated Spotipy client instance.
        playlist_id (str): The ID of the playlist to which tracks will be added.
        song_recommendations (list): A list of dictionaries representing song recommendations.
    
    Returns:
        None
    """
    track_uris = []
    
    # Iterate over each recommended song and search for its Spotify track URI
    for song in song_recommendations:
        # Build a search query using the song name and artist
        query = f"track:{song.get('name', '')} artist:{song.get('artist', '')}"
        result = sp.search(q=query, type='track', limit=1)
        tracks = result.get('tracks', {}).get('items', [])
        if tracks:
            track_uris.append(tracks[0]['uri'])
    
    # If any track URIs were found, add them to the playlist.
    if track_uris:
        sp.playlist_add_items(playlist_id, track_uris)