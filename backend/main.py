from backend.models import *
from backend.utils import *

def process_images(student_img_path, instructor_img_path, prompt_path, csv_path):
    student_response = process_form(prompt_path, student_img_path)
    instructor_response = process_form(prompt_path, instructor_img_path)
    dict_to_csv(student_response, csv_path)
    add_instruct_answer_to_csv(instructor_response, csv_path)

def evaluate_question(question, student_answer, instructor_answer):
    gpt3_model = TextModel(model_name="gpt-3.5-turbo-0125")
    router_prompt = (f"Given the question: '{question}', evaluate if the student's answer: '{student_answer}' "
              f"is 100% correct against the instructor's answer: '{instructor_answer}'. "
              f"Return '(correct:1)' if the student's answer is fully correct, or '(correct:0)'\
                  if the answer is incorrect or if you are unsure.")
    first_evaluation = gpt3_model.complete(prompt=router_prompt, role="user")
    eval_result = 1 if "(correct:1)" in first_evaluation else 0
    if eval_result: return "Correct answer", True

    gpt4_model = TextModel(model_name="gpt-4-1106-preview")
    cot_prompt = (
        f"Given the question: '{question}', evaluate step by step and succinctly answer why the student's answer: '{student_answer}' "
              f"is partially or completely wrong against the instructor's answer: '{instructor_answer}'. "
    )
    second_evaluation = gpt4_model.complete(cot_prompt)
    return second_evaluation, False
