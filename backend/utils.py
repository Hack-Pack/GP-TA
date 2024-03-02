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
    
# vision_model = VisionModel()
# prompt = """I'll provide you images that has math questions and their respective answers, format them into a JSON object where each question is a key and its corresponding answer is the value.
#             Ensure that each key-value pair is correctly formatted according to JSON standards.
#             Note: The answers should contain each and every step, do not skip anything.
#             Note: Do not add any information of answers other than what is written/present.
            
#             Here is the example format on how your response should be shown as below.
#             Note: Replace the values in <> by the appropriate string values from the context.
#             The format:
#             {
#             <Question 1>: <Complete Solution 1>,
#             <Question 2>: <Complete Solution 2>,
#             <Question 3>: <Complete Solution 3>,
#             <Question 4>: <Complete Solution 4>,            
#             }
#         """

# Instructor
img_path = "/Users/pavan/Desktop/Hackathon/GP-TA/data/instructor_images"
out_path = "/Users/pavan/Desktop/Hackathon/GP-TA/data/instructor.json"
prompt_path = "/Users/pavan/Desktop/Hackathon/GP-TA/prompts/csv_promt.txt"
csv_output = "/Users/pavan/Desktop/Hackathon/GP-TA/output.csv"

response = process_form(prompt_path, img_path)
print(response)

json_to_csv(response, csv_output)

# Student
img_path = "/Users/pavan/Desktop/Hackathon/GP-TA/data/student_images"
out_path = "/Users/pavan/Desktop/Hackathon/GP-TA/data/student.json"

response = process_form(prompt_path, img_path)
print(response)

add_answers_to_csv(response, csv_output)
