import os
from dotenv import load_dotenv

# Load environment variables from a .env file if available
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "your_spotify_client_id")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "your_spotify_client_secret")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8501/callback")

# Additional configuration for Agno integration
AGNO_API_KEY = os.getenv("AGNO_API_KEY", "your_agno_api_key")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_groq_api_key")