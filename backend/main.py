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
    input_text = f"You are kindhearted middle school teacher. Based on the following student performance:\n{string_representation}\nPlease generate a succinct 2-3 sentence summary of the student's performance, highlighting strengths and weaknesses. And give encouraging feedback for next steps in 1-2 sentences to finish. Be conversational and start with: Hey Kenny..."
    gpt4_model = TextModel(model_name="gpt-4-1106-preview")
    response_text = gpt4_model.complete(input_text)
    # Call the tts function with the formatted string
    tts(response_text)

    return response_text