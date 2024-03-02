import json
import pandas as pd
from models import VisionModel

def json_to_csv(json_data, csv_file):    
    data = json.loads(json_data)
        
    ids = []
    questions = []
    answers = []
    
    # Iterate through each key-value pair in the JSON data
    for key, value in data.items():            
        question = key
        answer = value
        
        # Generate id based on the index of the key
        _id = key[1:key.find(':')]
                            
        ids.append(_id)
        questions.append(question)
        answers.append(answer)
            
    df = pd.DataFrame({
        'id': ids,
        'question': questions,
        'answer': answers
    })
        
    df.to_csv(csv_file, index=False)
    
def add_answers_to_csv(answers_json, csv_file):    
    answers_data = json.loads(answers_json)
    
    df = pd.read_csv(csv_file)
    
    answers = []

    # Iterate through each row in the DataFrame and append the corresponding answer
    for answer in answers_data.values():                        
        answers.append(answer)
    
    df['student_answer'] = answers

    df.to_csv(csv_file, index=False)
    
def process_form(prompt_path, img_path):
    try:
        vision_model = VisionModel()
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()
        response = vision_model.complete(prompt, img_path)
        return response
    except Exception as e:
        print(f"An error occurred: {e}")

# Instructor
# img_path = "data/instructor_images"
# out_path = "data/instructor.json"
# prompt_path = "prompts/csv_promt.txt"
# csv_output = "output.csv"

# response = process_form(prompt_path, img_path)
# print(response)

# json_to_csv(response, csv_output)

# # Student
# img_path = "data/student_images"
# out_path = "data/student.json"

# response = process_form(prompt_path, img_path)
# print(response)

# add_answers_to_csv(response, csv_output)
