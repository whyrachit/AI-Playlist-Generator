import os
from dotenv import load_dotenv

# Load environment variables from a .env file if available
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Additional configuration for Agno integration
AGNO_API_KEY = os.getenv("AGNO_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")