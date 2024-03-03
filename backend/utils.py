import json
import pandas as pd
import numpy as np
import re
from openai import OpenAI
from backend.models import *

def dict_to_csv(dictionary, csv_file_path):
    # Initialize a list to hold the rows of the DataFrame
    rows = []
    
    # Iterate through the dictionary to extract each question and its details
    for question_id, details in dictionary.items():
        for question, student_answer in details.items():
            # Convert question_id to integer (strip 'Q' and convert to int)
            q_id = int(question_id.strip('Q'))
            # Append the extracted information as a row in the list
            rows.append({
                'question_id': q_id,
                'question': question,
                'student_answer': student_answer
            })
    
    # Convert the list of rows into a DataFrame
    df = pd.DataFrame(rows)
    df["question_id"] = df["question_id"].astype(int)
    
    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)
    
def add_instruct_answer_to_csv(dictionary, csv_file_path):
    # Load the CSV file
    df = pd.read_csv(csv_file_path)
    solutions = []
    for question, details in dictionary.items():
        for problem, solution in details.items():
            solutions.append(solution)
    # Create the new column and populate it
    df['instructor_answer'] = solutions
    df.to_csv(csv_file_path, index=False)

def extract_content(string):
    start_index = string.find("{")  # Find the index of the first "{"
    end_index = string.rfind("}")   # Find the index of the last "}"
    
    if start_index == -1 or end_index == -1:  # If either "{" or "}" is not found
        return None
    
    return string[start_index:end_index + 1] 
    
def process_form(prompt_path, img_path):

    vision_model = VisionModel()
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()
    response = vision_model.complete(prompt, img_path)
    dict_object = json.loads(extract_content(response))

    return dict_object

def read_embeddings(csv_path):
    df = pd.read_csv(csv_path)
    # Assuming embeddings are stored as string representations of lists
    df['embedding'] = df['embedding'].apply(lambda x: np.fromstring(x.strip("[]"), sep=','))
    return df

# Function to manually compute cosine similarity
def cosine_similarity_manual(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)
    return similarity

# Function to compute cosine similarity and return top k matches
def top_k_matched_questions(query, k=5):
    # Path to the CSV file
    csv_path = 'backend/embedded_questions.csv'
    questions_df = read_embeddings(csv_path)
    
    # Get embedding for the query
    query_embedding = get_embedding(query)  # Assuming get_embedding is defined elsewhere and set up properly
    
    # Compute similarities
    similarities = np.array([cosine_similarity_manual(query_embedding, np.array(embedding)) for embedding in questions_df['embedding']])
    
    # Get top k indices
    top_k_indices = similarities.argsort()[-k:][::-1]
    
    # Return the top k matched questions
    return questions_df.iloc[top_k_indices]['question'].tolist()

# Function to get embeddings
def get_embedding(text, model="text-embedding-3-small"):
    client = OpenAI()
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding
