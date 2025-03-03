import streamlit as st

def inject_custom_css():
    """
    Injects custom CSS for a Spotify-like UI globally.
    """
    st.markdown("""
    <style>
        .stApp {
            background-color: #191414;
        }
        h1, h2, h3, h4, h5, h6, .css-ffhzg2, .css-1lsmgbg {
            color: white;
        }
        .stTextInput>div>div>input {
            background-color: #282828;
            color: white;
            border: 1px solid #1DB954;
        }
        .stButton>button {
            background-color: #1DB954;
            color: white;
            border: none;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px 20px;
        }
        .spotify-logo {
            width: 200px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<img src="https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg" class="spotify-logo">',
        unsafe_allow_html=True
    )

def display_interface():
    """
    Renders the Spotify-inspired UI for the Spotify Playlist Generator.
    It collects the user's prompt.
    
    Returns:
        user_prompt (str): The prompt entered by the user.
    """
    st.title("Spotify Playlist Generator")
    st.write("Enter a prompt describing the playlist you want to generate.")

    # Text input for the user's prompt.
    user_prompt = st.text_input(
        "Playlist Prompt", 
        placeholder="A Bollywood breakup playlist with artists like Arijit Singh and Atif Aslam"
    )

    return user_prompt
