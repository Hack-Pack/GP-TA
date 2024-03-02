import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import streamlit as st
from utils import *

# Set wide mode
st.set_page_config(layout="wide")

# Page navigation
page = st.sidebar.selectbox("Choose a page", ["Homepage", "Feedback"])

if page == "Homepage":
    st.title("Homepage")

    #Upload functions for the sidebar
    uploaded_assignments = st.sidebar.file_uploader("Upload Assignments", accept_multiple_files= True, type=None)  # You can specify types with the 'type' parameter
    if uploaded_assignments:
        st.sidebar.write("You have uploaded a file.")

    uploaded_rubric = st.sidebar.file_uploader("Upload Rubric", type=None)  # You can specify types with the 'type' parameter
    if st.sidebar.button("Upload Files"):
        if uploaded_assignments and uploaded_rubric:

            #Handle the uploaded files


            st.sidebar.write("Files have been successfully uploaded.")
            
    
    #Display the uploaded files
        
    col1, col2 = st.columns(2)
    with col1:
        st.write("This is column 1")
        st.image("testing_data/kitty.jpg", width=400)

    with col2:
        st.write("This is column 2")
        st.text_area("This is a text area", "Hello, World!")
        

elif page == "Feedback":

    st.title("Feedback")

    

    # Adding an audio player
    st.write("Listen to our feedback request:")
    audio_file = open('testing_data/speech.mp3', 'rb')  # Update the path to your audio file
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3', start_time=0)