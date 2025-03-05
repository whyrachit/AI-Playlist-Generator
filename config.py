import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:5000")

# Additional configuration for Agno integration
AGNO_API_KEY = os.getenv("AGNO_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Removed Cache Settings (CACHE_TTL and any related constants)

if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET and GEMINI_API_KEY:
    logger.info("All required API credentials are configured")
else:
    missing_creds = []
    if not SPOTIFY_CLIENT_ID:
        missing_creds.append("SPOTIFY_CLIENT_ID")
    if not SPOTIFY_CLIENT_SECRET:
        missing_creds.append("SPOTIFY_CLIENT_SECRET")
    if not GEMINI_API_KEY:
        missing_creds.append("GROQ_API_KEY")
    logger.warning(f"Missing required credentials: {', '.join(missing_creds)}")
