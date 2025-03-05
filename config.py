import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to load secrets from Streamlit (st.secrets) if available,
# otherwise fallback to using environment variables loaded via .env.
try:
    import streamlit as st
    # If running in a Streamlit environment, use st.secrets.
    SPOTIFY_CLIENT_ID = st.secrets.spotify.client_id
    SPOTIFY_CLIENT_SECRET = st.secrets.spotify.client_secret
    SPOTIFY_REDIRECT_URI = st.secrets.spotify.redirect_uri
    GEMINI_API_KEY = st.secrets.gemini.api_key
    logger.info("Loaded API credentials from Streamlit secrets")
except ImportError:
    # Fallback: load environment variables from a .env file.
    from dotenv import load_dotenv
    load_dotenv()
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    logger.info("Loaded API credentials from environment variables (.env)")

# Check if required credentials are configured.
if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET and GEMINI_API_KEY:
    logger.info("All required API credentials are configured")
else:
    missing_creds = []
    if not SPOTIFY_CLIENT_ID:
        missing_creds.append("SPOTIFY_CLIENT_ID")
    if not SPOTIFY_CLIENT_SECRET:
        missing_creds.append("SPOTIFY_CLIENT_SECRET")
    if not GEMINI_API_KEY:
        missing_creds.append("GEMINI_API_KEY")
    logger.warning(f"Missing required credentials: {', '.join(missing_creds)}")
