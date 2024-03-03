import os
import streamlit as st
import base64
from pdf2image import convert_from_bytes, convert_from_path


def save_uploaded_file(uploaded_file, directory):
    if uploaded_file is not None:
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Convert PDF pages to images
        images = convert_from_bytes(uploaded_file.getbuffer())

        image_paths = []
        # Save each page as an image
        for i, image in enumerate(images):
            image_path = os.path.join(directory, f"{uploaded_file.name}_page_{i+1}.png")
            image_paths.append(image_path)
            image.save(image_path, "PNG")

    return image_paths


# Function to display images from a directory or a default image if the directory is empty
def display_images(file_paths, default_image_path, title):
    images = file_paths  # List all images in the directory
    if len(images) > 0:
        for image_path in images:
            st.image(image_path, width=500)  # Adjust width as needed
    else:
        # Display default image if no images are found
        st.image(default_image_path, caption="Default Image", width=500)
        
def read_video_csv(df):
    # Prepare the context for GPT based on video names and their links
    context = "Based on the following video titles and their links:\n"
    for _, row in df.iterrows():
        question = row['question']
        video_link = row['link']
        context += f"- {question}: {video_link}\n"
    return context 