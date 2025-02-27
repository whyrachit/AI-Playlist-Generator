import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

def spotify_authenticate():
    """
    Authenticates the user with Spotify via OAuth and returns an authenticated Spotipy client.
    Handles the OAuth callback automatically.
    """
    scope = "playlist-modify-private playlist-modify-public"
    
    # Initialize OAuth in session state if not exists
    if 'sp_oauth' not in st.session_state:
        st.session_state.sp_oauth = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=scope,
            cache_path=".spotifycache"
        )

    # Check for existing token
    token_info = st.session_state.sp_oauth.get_cached_token()
    
    # If no valid token, check for callback code
    if not token_info:
        query_params = st.query_params
        code = query_params.get("code", [None])[0]
        
        if code:
            try:
                # Get access token using the code
                token_info = st.session_state.sp_oauth.get_access_token(code)
                st.session_state.token_info = token_info
                st.query_params.clear()  # Clear URL params
            except Exception as e:
                st.error(f"Authentication failed: {str(e)}")
                return None
        else:
            # Show login button if no token and no code
            auth_url = st.session_state.sp_oauth.get_authorize_url()
            st.markdown(f"[Login to Spotify]({auth_url})")
            return None

    # Check token expiration
    if st.session_state.sp_oauth.is_token_expired(token_info):
        token_info = st.session_state.sp_oauth.refresh_access_token(
            token_info['refresh_token']
        )
        st.session_state.token_info = token_info

    if token_info and token_info.get("access_token"):
        return spotipy.Spotify(auth=token_info["access_token"])
    
    return None