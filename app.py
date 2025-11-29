from flask import Flask, request, render_template_string, session, redirect, url_for
import random
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Sample question and career data
questions = [
    {"text": "Do you enjoy solving logical problems?", "tags": ["analytical"]},
    {"text": "Do you prefer helping people with emotional issues?", "tags": ["empathetic"]},
    {"text": "Do you like working with your hands?", "tags": ["hands-on"]},
    {"text": "Are you interested in technology?", "tags": ["technical"]},
    {"text": "Do you enjoy writing or storytelling?", "tags": ["creative"]},
    {"text": "Do you enjoy leading a team?", "tags": ["leadership"]},
    {"text": "Are you comfortable with public speaking?", "tags": ["communication"]},
    {"text": "Do you enjoy detailed work and documentation?", "tags": ["detail-oriented"]},
    {"text": "Do you like designing things?", "tags": ["design"]},
    {"text": "Do you enjoy teaching others?", "tags": ["educational"]},
    {"text": "Would you rather work outdoors?", "tags": ["outdoors"]},
    {"text": "Do you enjoy working with data?", "tags": ["analytical"]},
    {"text": "Do you want to make a difference in people's lives?", "tags": ["empathetic"]},
    {"text": "Do you enjoy programming?", "tags": ["technical"]},
    {"text": "Do you enjoy performing arts?", "tags": ["creative"]},
    {"text": "Do you feel comfortable handling responsibility?", "tags": ["leadership"]},
    {"text": "Do you like organizing information?", "tags": ["detail-oriented"]},
    {"text": "Do you enjoy brainstorming new ideas?", "tags": ["creative"]},
    {"text": "Are you good at fixing things?", "tags": ["hands-on"]},
    {"text": "Do you like helping others learn?", "tags": ["educational"]},
    {"text": "Do you like spending time with animals?", "tags": ["empathetic"]},
    {"text": "Would you enjoy capturing photos or videos?", "tags": ["creative"]},
    {"text": "Do you enjoy exploring how machines work?", "tags": ["technical"]},
    {"text": "Do you enjoy creating art or graphics?", "tags": ["design"]},
    {"text": "Would you enjoy managing people or teams?", "tags": ["leadership"]},
]

careers = [
    {"name": "Software Developer", "description": "Designs, builds, and maintains software applications.", "tags": ["technical", "analytical"]},
    {"name": "Therapist", "description": "Helps individuals manage and overcome emotional challenges.", "tags": ["empathetic"]},
    {"name": "Mechanical Engineer", "description": "Designs and maintains mechanical systems.", "tags": ["hands-on", "technical"]},
    {"name": "Data Analyst", "description": "Analyzes data to help companies make better decisions.", "tags": ["analytical"]},
    {"name": "Graphic Designer", "description": "Creates visual content for branding and marketing.", "tags": ["creative", "design"]},
    {"name": "Teacher", "description": "Educates students in various subjects.", "tags": ["educational", "empathetic"]},
    {"name": "Manager", "description": "Leads teams and coordinates work to reach goals.", "tags": ["leadership"]},
    {"name": "Veterinarian", "description": "Treats and cares for animals.", "tags": ["empathetic"]},
    {"name": "Architect", "description": "Designs buildings and oversees construction.", "tags": ["design", "creative"]},
    {"name": "Electrician", "description": "Installs and maintains electrical systems.", "tags": ["hands-on"]},
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'step' not in session:
        session['step'] = 0
        session['scores'] = defaultdict(int)
        session['asked'] = []

    step = session['step']
    scores = session['scores']
    asked = session['asked']

    if request.method == 'POST':
        answer = request.form.get('answer', '').strip().lower()
        if answer in ['yes', 'y']:
            for tag in questions[asked[-1]]['tags']:
                scores[tag] += 1
        elif answer not in ['no', 'n']:
            error = "Please respond with 'yes' or 'no'."
            return render_template_string(TEMPLATE, question=questions[asked[-1]]['text'], error=error)

    if len(asked) >= 25:
        # Determine best career match
        def match_score(career):
            return sum(scores.get(tag, 0) for tag in career['tags'])

        best = sorted(careers, key=match_score, reverse=True)[:5]
        session.clear()
        return render_template_string(RESULT_TEMPLATE, careers=best)

    # Pick a new question
    available = [i for i in range(len(questions)) if i not in asked]
    if not available:
        session.clear()
        return render_template_string("<p>Not enough questions to proceed.</p>")

    next_q = random.choice(available)
    asked.append(next_q)
    session['asked'] = asked
    session['step'] = step + 1
    session['scores'] = scores
    return render_template_string(TEMPLATE, question=questions[next_q]['text'], error=None)

TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Career AI Chat</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; display: flex; justify-content: center; padding: 50px; }
        .chat-box { background: white; padding: 20px; width: 500px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input[type=text] { width: 100%; padding: 10px; margin-top: 10px; }
        input[type=submit] { padding: 10px 20px; background: #007bff; color: white; border: none; margin-top: 10px; cursor: pointer; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="chat-box">
        <h2>Career AI</h2>
        <p>{{ question }}</p>
        {% if error %}<p class="error">{{ error }}</p>{% endif %}
        <form method="post">
            <input type="text" name="answer" placeholder="yes or no" autofocus>
            <input type="submit" value="Send">
        </form>
    </div>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Career Match Results</title>
    <style>
        body { font-family: Arial; background: #eef2f7; padding: 30px; }
        .result-box { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <h1>Top Career Matches</h1>
    {% for career in careers %}
        <div class="result-box">
            <h2>{{ career.name }}</h2>
            <p>{{ career.description }}</p>
        </div>
    {% endfor %}
    <a href="/">Start Over</a>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=False)
