import json
import pandas as pd
import re
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
