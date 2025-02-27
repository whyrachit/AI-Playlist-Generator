import streamlit as st
from ui.interface import display_interface
from agent.prompt_processor import process_prompt
from spotify.auth import spotify_authenticate
from spotify.playlist import create_spotify_playlist, add_tracks_to_playlist

def main():
    st.set_page_config(page_title="Spotify Playlist Generator", layout="wide")

    if st.query_params.get("code"):
        spotify_authenticate()

    # 1. Collect user prompt via the interface.
    user_prompt = display_interface()
    
    # 2. Generate playlist (process prompt) when "Generate Playlist" is clicked.
    if st.button("Generate Playlist"):
        if user_prompt:
            st.info("Processing your prompt to generate the playlist...")
            song_suggestions = process_prompt(user_prompt)
            st.session_state['playlist_details'] = song_suggestions
            st.success("Playlist generated!")
        else:
            st.warning("Please enter a prompt.")
    
    # 3. Button to show the generated playlist.
    if st.button("Show Generated Playlist"):
        if 'playlist_details' in st.session_state and st.session_state['playlist_details']:
            st.subheader("Generated Playlist")
            for idx, song in enumerate(st.session_state['playlist_details'], start=1):
                song_name = song.get("name", "Unknown Song")
                artist_name = song.get("artist", "Unknown Artist")
                st.markdown(f"- **{idx}. {song_name}** by *{artist_name}*")
        else:
            st.warning("No playlist generated yet. Please generate a playlist first.")
    
    # 4. Button for Spotify authentication and playlist creation.
    if st.button("Create Playlist in Spotify"):
        st.info("Initiating Spotify authentication...")
        sp = spotify_authenticate()
        if sp:
            st.info("Creating your new playlist...")
            playlist_id = create_spotify_playlist(
                sp, 
                playlist_name="My Generated Playlist", 
                description="Playlist created using the Spotify Playlist Generator"
            )
            add_tracks_to_playlist(sp, playlist_id, st.session_state.get('playlist_details', []))
            st.success("Playlist successfully created in your Spotify account!")
        else:
            st.error("Spotify authentication failed. Please try again.")

if __name__ == '__main__':
    main()
