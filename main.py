# main.py

from flask import Flask, request, render_template
import json
import random

app = Flask(__name__)

# Load questions and careers
with open('questions.json') as qf:
    ALL_QUESTIONS = json.load(qf)

with open('careers.json') as cf:
    CAREERS = json.load(cf)

# Function to compute matching scores
def score_user_answers(answers):
    scores = []
    for career in CAREERS:
        score = 0
        for q_id, user_answer in answers.items():
            traits = career['traits']
            if q_id in traits:
                expected = traits[q_id]
                # If answer matches expectation, add score
                if expected == user_answer:
                    score += 1
        scores.append((score, career))
    scores.sort(reverse=True, key=lambda x: x[0])
    return scores[:5]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_answers = {}
        for q in ALL_QUESTIONS[:25]:
            user_input = request.form.get(q['id'])
            if user_input:
                user_answers[q['id']] = user_input.lower() == 'yes'

        top_careers = score_user_answers(user_answers)
        return render_template('result.html', careers=top_careers)

    selected_questions = random.sample(ALL_QUESTIONS, 25)
    return render_template('index.html', questions=selected_questions)

if __name__ == '__main__':
    app.run(debug=False)
