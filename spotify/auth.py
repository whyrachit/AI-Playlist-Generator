import uuid
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

def show_login_button():
    if 'sp_oauth' not in st.session_state:
        st.error("OAuth client not initialized")
        return

    auth_url = st.session_state.sp_oauth.get_authorize_url()
    button_html = f"""
    <a href="{auth_url}">
        <button style="
            background-color: #1DB954;
            color: white;
            border: none;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
        ">
            Login to Spotify
        </button>
    </a>
    """
    st.markdown(button_html, unsafe_allow_html=True)

def spotify_authenticate():
    scope = "playlist-modify-private playlist-modify-public user-read-private user-read-email"
    
    if 'spotify_cache_path' not in st.session_state:
        st.session_state.spotify_cache_path = f".spotifycache-{uuid.uuid4()}"

    if 'sp_oauth' not in st.session_state:
        st.session_state.sp_oauth = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=scope,
            cache_path=st.session_state.spotify_cache_path,
            show_dialog=True
        )

    # Token validation check
    if 'token_info' in st.session_state:
        try:
            sp = spotipy.Spotify(auth=st.session_state.token_info['access_token'])
            sp.current_user()  # Test authentication
        except Exception:
            st.session_state.pop('token_info', None)
            st.rerun()  # Updated here

    query_params = st.query_params
    code = query_params.get("code")

    if code and "code_processed" not in st.session_state:
        try:
            token_info = st.session_state.sp_oauth.get_access_token(code)
            st.session_state.token_info = token_info
            st.session_state.code_processed = True
            st.rerun()  # Updated here
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            st.session_state.pop("token_info", None)
            return None

    token_info = st.session_state.get("token_info")

    if not token_info:
        show_login_button()
        return None

    if st.session_state.sp_oauth.is_token_expired(token_info):
        try:
            token_info = st.session_state.sp_oauth.refresh_access_token(
                token_info['refresh_token']
            )
            st.session_state.token_info = token_info
        except Exception as e:
            st.error(f"Token refresh failed: {str(e)}")
            st.session_state.pop("token_info", None)
            show_login_button()
            return None

    return spotipy.Spotify(auth=token_info["access_token"])