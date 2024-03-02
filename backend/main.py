from models import *
from utils import *

def process_images(student_img_path, instructor_img_path, prompt_path, csv_path):
    student_response = process_form(prompt_path, student_img_path)
    instructor_response = process_form(prompt_path, instructor_img_path)
    dict_to_csv(student_response, csv_path)
    add_instruct_answer_to_csv(instructor_response, csv_path)


def evaluate_question(question, student_answer, instructor_answer):
    model = TextModel()
    prompt = (f"Given the question: '{question}', evaluate the student's answer: '{student_answer}' "
              f"against the instructor's answer: '{instructor_answer}'. Provide a detailed analysis.")

    evaluation = model.complete(prompt=prompt, role="user")
    return evaluation