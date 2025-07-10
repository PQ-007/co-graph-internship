import streamlit as st

st.subheader("1. Embedding a Video from After Effects")

st.write("First, render your After Effects composition to a web-friendly video format like MP4 or WebM.")

# Assuming your video file is named 'my_animation.mp4' and is in the same directory as your Streamlit app
# Or provide a full path: '/path/to/your/video/my_animation.mp4'
video_file_path = "my_animation.mp4"

try:
    with open(video_file_path, "rb") as video_file:
        video_bytes = video_file.read()
        st.video(video_bytes)
except FileNotFoundError:
    st.error(f"Video file '{video_file_path}' not found. Please place it in the same directory or provide the correct path.")
except Exception as e:
    st.error(f"An error occurred loading the video: {e}")

st.caption("Place your exported .mp4 (or .webm) file in your project directory.")