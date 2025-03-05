import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from a .env file if available
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:5000")

# Additional configuration for Agno integration
AGNO_API_KEY = os.getenv("AGNO_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Cache settings
CACHE_TTL = 3600  # 1 hour cache for API responses
MAX_RETRIES = 3   # Maximum retries for API calls

# Log configuration status
if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET and GROQ_API_KEY:
    logger.info("All required API credentials are configured")
else:
    missing_creds = []
    if not SPOTIFY_CLIENT_ID:
        missing_creds.append("SPOTIFY_CLIENT_ID")
    if not SPOTIFY_CLIENT_SECRET:
        missing_creds.append("SPOTIFY_CLIENT_SECRET")
    if not GROQ_API_KEY:
        missing_creds.append("GROQ_API_KEY")
    logger.warning(f"Missing required credentials: {', '.join(missing_creds)}")