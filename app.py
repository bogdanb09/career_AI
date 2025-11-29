from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# Simple yes/no questions and corresponding traits
questions = [
    ("Do you enjoy solving complex problems?", "analytical"),
    ("Are you interested in helping people with their emotions?", "empathetic"),
    ("Do you like working with your hands?", "practical"),
    ("Are you comfortable speaking in front of groups?", "leader"),
    ("Do you prefer creative activities like drawing or writing?", "creative"),
    ("Do you enjoy teaching others?", "educator"),
    ("Would you like to work with animals?", "animal_lover"),
    ("Do you enjoy using computers or coding?", "tech"),
    ("Are you interested in science or medicine?", "scientific"),
    ("Do you prefer jobs with a clear routine?", "structured"),
    # Add more if needed up to 100
]

# Simple career mapping based on traits
career_matches = {
    "tech": "Software Developer",
    "analytical": "Data Analyst",
    "empathetic": "Therapist",
    "leader": "Project Manager",
    "practical": "Electrician",
    "creative": "Graphic Designer",
    "educator": "Teacher",
    "animal_lover": "Veterinarian",
    "scientific": "Biologist",
    "structured": "Accountant"
}

# Store responses temporarily
user_answers = {}

@app.route('/')
def start():
    user_answers.clear()
    return redirect(url_for('question', q=0))

@app.route('/question/<int:q>', methods=['GET', 'POST'])
def question(q):
    if q >= len(questions):
        return redirect(url_for('result'))

    if request.method == 'POST':
        answer = request.form.get('answer')
        trait = questions[q][1]
        if answer == "yes":
            user_answers[trait] = user_answers.get(trait, 0) + 1
        return redirect(url_for('question', q=q + 1))

    question_text = questions[q][0]
    return f"""
    <h2>Question {q + 1} of {len(questions)}</h2>
    <p>{question_text}</p>
    <form method="post">
        <button type="submit" name="answer" value="yes">Yes</button>
        <button type="submit" name="answer" value="no">No</button>
    </form>
    """

@app.route('/result')
def result():
    if not user_answers:
        return redirect(url_for('start'))

    best_trait = max(user_answers, key=user_answers.get)
    career = career_matches.get(best_trait, "Undetermined")

    return f"""
    <h1>Your Suggested Career:</h1>
    <h2>{career}</h2>
    <p>Based on your answers, a career as a <strong>{career}</strong> might be a great fit for you!</p>
    <a href="/">Start Over</a>
    """

if __name__ == '__main__':
    app.run(debug=True)
