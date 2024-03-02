from models import *
from utils import *

def process_images(student_img_path, instructor_img_path, prompt_path, csv_path):
    student_response = process_form(prompt_path, student_img_path)
    instructor_response = process_form(prompt_path, instructor_img_path)
    dict_to_csv(student_response, csv_path)
    add_instruct_answer_to_csv(instructor_response, csv_path)


def evaluate_question(question, student_answer, instructor_answer):
    gpt3_model = TextModel(model="gpt-3.5-turbo-0125")
    router_prompt = (f"Given the question: '{question}', evaluate if the student's answer: '{student_answer}' "
              f"is 100% correct against the instructor's answer: '{instructor_answer}'. "
              f"Return '(correct:1)' if the student's answer is fully correct, or '(correct:0)' if the answer is incorrect or if you are unsure.")

    first_evaluation = gpt3_model.complete(prompt=router_prompt, role="user")
    eval_result = eval(first_evaluation.text.strip())

    return eval_result