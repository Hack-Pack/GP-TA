import sys
from pathlib import Path
import csv
import pandas as pd
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import streamlit as st
from utils import *
from backend.main import process_images, evaluate_question

# FILE PATHS
PROMPT_PATH = "prompts/csv_promt.txt"
CSV_PATH = "backend/out.csv"
STUDENT_IMAGES = "data/student_images"
INSTRUCTOR_IMAGES = "data/instructor_images"
DEFAULT_IMAGE_PATH = "frontend/testing_data/placeholder.png"
VOICE_TESTING = "frontend/testing_data/speech.mp3"
LOGO = "frontend/testing_data/logo.png"

# Initialize state variables if not already present
if "student_images_paths" not in st.session_state:
    st.session_state.student_images_paths = []

if "instructor_images_path" not in st.session_state:
    st.session_state.instructor_images_path = []

# Set wide mode
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage], [data-testid=stSidebar] .markdown-text-container {
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        html, body, [class*="st-"] {
            font-size: 20px;
        }
        [class*="st-"] p {
            font-size: 16px;
        }
    </style>
    """, unsafe_allow_html=True
)

with st.sidebar:
    st.image(LOGO, width=200)  # Placeholder for a logo
    st.markdown("""<h1 style = "text-align: center">Guided Sprout</h1>""", unsafe_allow_html=True)

        # Page navigation
    page = st.selectbox("Choose a page", ["Homepage", "Table"])

    with st.expander("Upload Section", expanded=False):  
        # Now, use regular st commands for widgets inside the expander
        uploaded_assignments = st.file_uploader(
            "Upload Assignments", accept_multiple_files=True, type=None
        )  # You can specify types with the 'type' parameter
        if uploaded_assignments:
            st.write("You have uploaded a file.")

        uploaded_rubric = st.file_uploader(
            "Upload Rubric", type=None
        )  # You can specify types with the 'type' parameter

        # The button should just be st.button(), not st.sidebar.button()
        if st.button("Upload Files"):
            if uploaded_assignments and uploaded_rubric:
                for uploaded_assignment in uploaded_assignments:
                    st.session_state.student_images_paths += save_uploaded_file(
                        uploaded_assignment, "data/student_images"
                    )

                st.session_state.instructor_images_path += save_uploaded_file(
                    uploaded_rubric, "data/instructor_images"
                )

                process_images(STUDENT_IMAGES, INSTRUCTOR_IMAGES, PROMPT_PATH, CSV_PATH)

                st.write("Files have been successfully uploaded.")




if page == "Homepage":
    col1, col2 = st.columns(2)
    with col1:
        tab1, tab2 = st.tabs(["Student Images", "Instructor Images"])

        with tab1:
            display_images(
                st.session_state.student_images_paths, DEFAULT_IMAGE_PATH, "Student"
            )

        with tab2:
            display_images(
                st.session_state.instructor_images_path,
                DEFAULT_IMAGE_PATH,
                "Instructor",
            )
            
    with col2:
        tab1, tab2 = st.tabs(["Evaluation", "Feedback"])
        with tab1:
            # Create an empty placeholder
            text_placeholder = st.empty()
            if st.button("Evaluate"):
                print(
                    st.session_state.student_images_paths,
                    st.session_state.instructor_images_path,
                )
                results = ""
                with open(CSV_PATH, mode="r", encoding="utf-8") as csv_file:
                    # Create a CSV reader object from the file object
                    csv_reader = csv.DictReader(csv_file)
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    # Iterate over each row in the CSV
                    for row in csv_reader:                        
                        question_id = row["question_id"]
                        question = row["question"]
                        student_answer = row["student_answer"]
                        instructor_answer = row["instructor_answer"]
                                                
                        status_text.text(f'Evaluating Question No: {question_id}')
                        evaluation_text, is_correct = evaluate_question(
                            question, student_answer, instructor_answer
                        )
                                                
                        # Choose color based on correctness
                        color = "green" if is_correct else "orange"
                        if is_correct:
                            time.sleep(3)
                            
                        question_placeholder = st.empty()
                        results = f"<br><strong>Question No: {question_id}</strong><br><span style='color: {color};'>{evaluation_text}</span><br>"
                        progress_bar.progress(int(question_id)*25)
                        status_text.text(f'Evaluated Question No: {question_id}')
                        st.toast(f'Evaluated Question No: {question_id}', icon='🪄')                                                                   

                        # Use st.markdown to render the HTML
                        text_placeholder.markdown(results, unsafe_allow_html=True)
                    
                    time.sleep(2)
                    status_text.text('Evaluation Done!')
                    st.toast('Hooray!', icon='🎉')
                                        
            with tab2:
                st.title("Feedback")
                text_placeholder = st.empty()
                
                # TODO: TTS
                # Adding an audio player
                st.write("Listen to our feedback request:")
                
                audio_file = open(
                    VOICE_TESTING, "rb"
                )  # Update the path to your audio file
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3", start_time=0)
                
                results = "🌟 Here are the recommended questions for improvement! Let's dive in and explore 🚀<ul>"
                with open(CSV_PATH, mode="r", encoding="utf-8") as csv_file:
                    # Create a CSV reader object from the file object
                    csv_reader = csv.DictReader(csv_file)
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    # TODO: Iterate over each row in the CSV
                    for row in csv_reader: 
                        question_id = row["question_id"]                                               
                        question = row["question"]
                        results += f"<li><strong>Question {question_id}:</strong> {question}</li>"
                        
                    results += "</ul>✨ Keep up the great work, and remember, every question is a step towards mastery! 📚"
                    
                text_placeholder.markdown(results, unsafe_allow_html=True)

    


elif page == "Table":
    st.title("Table")
    df = pd.read_csv(CSV_PATH)
    st.dataframe(df)
