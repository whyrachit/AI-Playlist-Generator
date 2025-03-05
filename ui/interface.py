import streamlit as st

def inject_custom_css():
    """
    Enhanced Spotify-inspired UI with modern styling.
    """
    st.markdown("""
    <style>
        /* Modern Spotify-inspired theme */
        .stApp {
            background: linear-gradient(180deg, #191414 0%, #121212 100%);
            color: #FFFFFF;
        }
        .main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 1.5rem;
        }

        /* Input fields */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #282828;
            color: white;
            border: 1px solid #1DB954;
            border-radius: 8px;
            padding: 0.75rem;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
            border-color: #1ed760;
            box-shadow: 0 0 0 2px rgba(29, 185, 84, 0.3);
        }

        /* Buttons */
        .stButton>button {
            background-color: #1DB954;
            color: white;
            border: none;
            font-weight: bold;
            border-radius: 500px;
            padding: 12px 24px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            width: 100%;
            margin: 10px 0;
        }
        .stButton>button:hover {
            background-color: #1ed760;
            transform: scale(1.02);
        }

        /* Cards */
        .playlist-card {
            background-color: #282828;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .playlist-card:hover {
            background-color: #3E3E3E;
            transform: translateY(-2px);
        }

        /* Status messages */
        .success-message {
            background-color: rgba(29, 185, 84, 0.1);
            border-left: 4px solid #1DB954;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }
        .error-message {
            background-color: rgba(226, 33, 52, 0.1);
            border-left: 4px solid #E22134;
            padding: 1rem;
            border-radius: 4px;
            margin: 1rem 0;
        }

        /* Loading animation */
        .loading-spinner {
            text-align: center;
            padding: 2rem;
        }
        .loading-spinner img {
            animation: spin 2s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Spotify logo */
        .spotify-logo {
            width: 180px;
            margin: 2rem auto;
            display: block;
            opacity: 0.9;
            transition: opacity 0.3s ease;
        }
        .spotify-logo:hover {
            opacity: 1;
        }
    </style>
    """, unsafe_allow_html=True)

    # Updated Spotify logo with better quality
    st.markdown(
        '<img src="https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_White.png" class="spotify-logo">',
        unsafe_allow_html=True
    )

def display_interface():
    """
    Enhanced Spotify Playlist Generator interface with improved UX.
    """
    st.title("✨ Spotify Playlist Generator")

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        playlist_name = st.text_input(
            "🎵 Playlist Name",
            placeholder="My Awesome Playlist",
            help="Give your playlist a unique name"
        )

        user_prompt = st.text_area(
            "🎧 Describe Your Perfect Playlist",
            placeholder=(
                "Example: Create a chill evening playlist with indie folk and acoustic songs, "
                "similar to artists like Bon Iver and Fleet Foxes, perfect for relaxing with a book"
            ),
            help="Be specific about the mood, genres, and artists you like",
            height=100
        )

    with col2:
        st.markdown("""
        ### 💡 Tips for Better Results

        Get the perfect playlist by including:
        - 🎸 Specific genres you love
        - 🎤 Favorite artists for inspiration
        - 🌟 The mood or vibe you want
        - 📅 Era or time period preferences
        - 🎯 Occasion (workout, relaxation, party)
        """)

    # Help text for better prompts
    st.markdown("""
    <div style='background-color: #282828; padding: 1rem; border-radius: 8px; margin: 1rem 0;'>
        <strong>🚀 Pro Tips:</strong><br>
        The more specific your description, the better the results! Try including:
        - Multiple artist references
        - Specific moods or emotions
        - Context for when you'll listen
        - Tempo preferences
        - Language or cultural elements
    </div>
    """, unsafe_allow_html=True)

    return playlist_name, user_prompt