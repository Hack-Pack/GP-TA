from backend.models import *
from backend.utils import *
import os

def process_images(student_img_path, instructor_img_path, prompt_path, csv_path):
    student_response = process_form(prompt_path, student_img_path)
    instructor_response = process_form(prompt_path, instructor_img_path)
    dict_to_csv(student_response, csv_path)
    add_instruct_answer_to_csv(instructor_response, csv_path)


def evaluate_question(question_id, question, student_answer, instructor_answer):
    PATH_OUT = 'backend/out.csv'
    # Assuming gpt3_model and gpt4_model are defined elsewhere in your script
    gpt3_model = TextModel(model_name="gpt-3.5-turbo-0125")
    router_prompt = (f"Given the question: '{question}', evaluate if the student's answer: '{student_answer}' "
              f"is 100% correct against the instructor's answer: '{instructor_answer}'. "
              f"Ensure the finals steps match and return '(correct:1)' if the student's answer is fully correct, or '(correct:0)' otherwise."
              f"if the answer is incorrect or if you are unsure.")
    first_evaluation = gpt3_model.complete(prompt=router_prompt, role="user")
    eval_result = 1 if "(correct:1)" in first_evaluation else 0
    
    # Load CSV file
    df = pd.read_csv(PATH_OUT)
    
    # Check if 'evaluation' column exists, if not add it
    if 'evaluation' not in df.columns:
        df['evaluation'] = 0
    
    # Update the DataFrame based on eval_result
    if eval_result == 1:
        evaluation_text = "Correct answer"
        evaluation_response = evaluation_text, True
    else:
        gpt4_model = TextModel(model_name="gpt-4-1106-preview")
        cot_prompt = (f"Given the question: '{question}', in 4 sentences answer why the student's answer: '{student_answer}' "
                      f"is partially or completely wrong against the instructor's answer, and do the evaluation step by step: '{instructor_answer}'.")
        evaluation_text = gpt4_model.complete(cot_prompt)
        evaluation_response = evaluation_text, False
        df.loc[df['question_id'] == int(question_id), 'evaluation'] = 1
    
    
    # Save the updated DataFrame back to CSV, overwriting the original file
    df.to_csv(PATH_OUT, index=False)

    return evaluation_response

def run_tts():
    # Assume tts function is defined elsewhere in your code
    # and pandas is already imported as pd

    # Load the DataFrame
    df = pd.read_csv('backend/out.csv')
    
    # Filter df to only "question" and "evaluation" columns
    filtered_df = df[['question', 'evaluation']]
    
    # Convert all rows in these columns to a single string representation
    # Each row's values are joined by a space, and rows are separated by a newline
    string_representation = '\n'.join(filtered_df.apply(lambda x: f"{x['question']} {x['evaluation']}", axis=1))
    
    # Format the string for the tts function, asking to generate a summary
    input_text = f"Based on the following student performance:\n{string_representation}\nPlease generate a succinct 4-5 sentence summary of the student's performance, highlighting strengths and weaknesses, that starts with: Hey Kenny, your performance on the exam was..."
    gpt4_model = TextModel(model_name="gpt-4-1106-preview")
    response_text = gpt4_model.complete(input_text)
    # Call the tts function with the formatted string
    tts(response_text)
    
def recommend_video_link(question, context):        
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Based on the video titles below, recommend the most relevant video for the question. If the question can't be answered based on the titles, then return empty string. Note: Only provide the link to the video and no additional text.\n\n" + context},
            {"role": "user", "content": f"Question: {question}\nAnswer:"}
        ],
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,    
    )
    return response.choices[0].message.content