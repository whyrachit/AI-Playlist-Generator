# Spotify Playlist Generator

An AI-powered tool that generates curated Spotify playlists based on your music preferences and mood! This app leverages real-time song details via Google Search and the Gemini API to produce a playlist of 20-25 hand-picked songs. Seamlessly integrated with Spotify, it allows you to create and save your custom playlists directly into your Spotify account.

## Live Demo

Experience the app live at: [Spotify Playlist Generator](https://spotifyai.streamlit.app)

## Features

- **AI-Curated Playlists:** Generate a curated list of songs based on your descriptive prompt.
- **Real-Time Song Data:** Fetch current song details using Google Search integrated within the agent.
- **Spotify Integration:** Authenticate with Spotify and save your generated playlists directly to your account.
- **User-Friendly UI:** Enjoy a modern, Spotify-inspired interface built with Streamlit.
- **Robust Error Handling:** Includes retry logic and fuzzy matching to ensure accurate song retrieval.

## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/whyrachit/AI-Playlist-Generator.git
   cd AI-Playlist-Generator
   ```
   
2. Create a Virtual Environment (Optional but Recommended):

   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install Dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application requires API credentials for Spotify and the Gemini API. You can configure these in one of two ways:

### Using Streamlit Secrets

If deploying on Streamlit Cloud, add your credentials in the secrets management:

```toml
client_id = "your_spotify_client_id"
client_secret = "your_spotify_client_secret"
redirect_uri = "your_spotify_redirect_uri"
api_key = "your_gemini_api_key"
```

### Using a .env File

Alternatively, create a .env file in the project root with the following variables:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=your_spotify_redirect_uri
GEMINI_API_KEY=your_gemini_api_key
```

The application will load these credentials at runtime.

## Running the App

Launch the Streamlit app by running:

```bash
streamlit run app.py
```
Then, open your browser and navigate to the localhost URL provided in the terminal.

## Folder Structure

```graphql
spotify-playlist-generator/
├── agent/
│   ├── __init__.py
│   └── prompt_processor.py     # Processes user prompts and generates song recommendations using Gemini API and Google Search
├── spotify/
│   ├── __init__.py
│   ├── auth.py                  # Handles Spotify OAuth authentication and login flow
│   └── playlist.py              # Manages Spotify playlist creation and adding tracks with retry logic
├── ui/
│   ├── __init__.py
│   └── interface.py             # Contains Streamlit UI components and custom CSS for a Spotify-inspired design
├── app.py                       # Main application file integrating all components
├── config.py                    # Manages API credentials configuration and environment setup
├── requirements.txt             # Lists all required Python packages
└── README.md                    # This file
```

## How It Works

User Input:

Provide a playlist name and a detailed description (e.g., mood, genres, favorite artists) in the app interface.
AI-Powered Playlist Generation:

The prompt_processor.py file uses an AI agent with live search capability to generate a playlist. It forces a Google Search call for real-time song data before curating 20-25 songs.
Spotify Integration:

The auth.py and playlist.py modules manage Spotify authentication and interact with Spotify’s API to create a new playlist and add the recommended tracks.
User Experience:

The UI, designed in interface.py, provides options to generate, preview, and save the playlist, all within an engaging, modern interface.

## Contributing

Contributions are welcome! If you have suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

Built with Streamlit
Integrated with the Spotify API via Spotipy
AI powered by Gemini API and enhanced by real-time Google Search


