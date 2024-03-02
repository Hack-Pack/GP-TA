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
        
        # Save each page as an image
        for i, image in enumerate(images):
            image_path = os.path.join(directory, f"{uploaded_file.name}_page_{i+1}.png")
            image.save(image_path, "PNG")

        
    return None
