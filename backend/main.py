from models import *

def evaluate_question(question, student_answer, instructor_answer):
    model = TextModel()
    prompt = (f"Given the question: '{question}', evaluate the student's answer: '{student_answer}' "
              f"against the instructor's answer: '{instructor_answer}'. Provide a detailed analysis.")
    
    evaluation = model.complete(prompt=prompt, role="user")
    return evaluation
