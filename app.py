import streamlit as st
from ui.interface import display_interface, inject_custom_css
from agent.prompt_processor import process_prompt
from spotify.auth import spotify_authenticate
from spotify.playlist import create_spotify_playlist, add_tracks_to_playlist

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    st.set_page_config(
        page_title="Spotify Playlist Generator",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Inject global CSS and logo for a Spotify-like UI
    inject_custom_css()
    
    # Initialize session state for progress tracking
    if 'processing_state' not in st.session_state:
        st.session_state.processing_state = None
    
    # Authenticate the user with Spotify
    sp = spotify_authenticate()
    if sp is None:
        return
    else:
        st.session_state["sp"] = sp
        if st.session_state.get('first_login', True):
            st.success("✅ Successfully connected to Spotify!")
            st.session_state.first_login = False
    
    # Display UI for playlist prompt and custom playlist name
    playlist_name, user_prompt = display_interface()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎵 Generate Playlist", key="generate"):
            if user_prompt:
                with st.spinner("🎧 Processing your prompt and fetching song recommendations..."):
                    st.session_state.processing_state = "generating"
                    song_suggestions = process_prompt(user_prompt)
                    st.session_state['playlist_details'] = song_suggestions
                    st.session_state.processing_state = "generated"
                st.success("✨ Playlist generated successfully!")
            else:
                st.warning("⚠️ Please enter a prompt to generate the playlist.")
    
    with col2:
        if st.button("👀 Preview Playlist", key="preview"):
            if 'playlist_details' in st.session_state and st.session_state['playlist_details']:
                st.subheader("🎵 Generated Playlist Preview")
                for idx, song in enumerate(st.session_state['playlist_details'], start=1):
                    with st.container():
                        st.markdown(
                            f"""
                            <div class="playlist-item">
                                <strong>{idx}. {song.get('name', 'Unknown Song')}</strong><br>
                                <em>by {song.get('artist', 'Unknown Artist')}</em>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.warning("⚠️ No playlist generated yet. Please generate a playlist first.")
    
    with col3:
        if st.button("💾 Save to Spotify", key="save"):
            if 'playlist_details' in st.session_state and st.session_state['playlist_details']:
                with st.spinner("📝 Creating your playlist on Spotify..."):
                    name_to_use = playlist_name if playlist_name else "My Generated Playlist"
                    try:
                        playlist_id = create_spotify_playlist(
                            st.session_state["sp"],
                            playlist_name=name_to_use,
                            description=f"Playlist created using AI: {user_prompt}"
                        )
                        add_tracks_to_playlist(
                            st.session_state["sp"],
                            playlist_id,
                            st.session_state['playlist_details']
                        )
                        st.success("🎉 Playlist successfully created in your Spotify account!")
                    except Exception as e:
                        st.error(f"❌ Error creating playlist: {str(e)}")
            else:
                st.warning("⚠️ No playlist to save. Please generate a playlist first.")

if __name__ == '__main__':
    main()
