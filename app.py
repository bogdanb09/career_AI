from flask import Flask, request, render_template_string, session, redirect, url_for
import json
import random

app = Flask(__name__)
app.secret_key = 'career-guidance-demo'

# Load data from JSON
with open("data.json", "r") as f:
    data = json.load(f)

questions = data["questions"]
careers = data["careers"]

# Extract all tags from the questions
all_tags = list({tag for q in questions for tag in q["tags"]})

@app.route("/", methods=["GET", "POST"])
def index():
    if "question_index" not in session:
        session["question_index"] = 0
        session["scores"] = {tag: 0 for tag in all_tags}
        session["asked"] = []

    if request.method == "POST":
        answer = request.form.get("answer", "").strip().lower()

        if answer not in ["yes", "no"]:
            return render_template_string(TEMPLATE, message="Please answer with yes or no.", question=session["current_question"]["text"])

        # Score based on answer
        if answer == "yes":
            for tag in session["current_question"]["tags"]:
                session["scores"][tag] += 1

        session["question_index"] += 1

    if session["question_index"] >= 25:
        # Rank careers based on score match
        ranked = []
        for career in careers:
            score = sum(session["scores"].get(tag, 0) * weight for tag, weight in career["traits"].items())
            ranked.append((score, career))

        ranked.sort(reverse=True, key=lambda x: x[0])
        top_careers = ranked[:5]
        session.clear()
        return render_template_string(RESULT_TEMPLATE, results=top_careers)

    # Choose a new question
    remaining_questions = [q for q in questions if q not in session["asked"]]
    if not remaining_questions:
        session.clear()
        return redirect(url_for("index"))

    question = random.choice(remaining_questions)
    session["current_question"] = question
    session["asked"].append(question)

    return render_template_string(TEMPLATE, message="", question=question["text"])


TEMPLATE = """
<!doctype html>
<title>Career AI</title>
<h1>Career Guidance AI</h1>
<p style="color: red;">{{ message }}</p>
<div style="font-family: Arial; background: #f4f4f4; padding: 20px; border-radius: 10px;">
  <form method="POST">
    <p><strong>Answer yes or no:</strong></p>
    <p>{{ question }}</p>
    <input name="answer" type="text" required>
    <button type="submit">Submit</button>
  </form>
</div>
"""

RESULT_TEMPLATE = """
<!doctype html>
<title>Your Career Matches</title>
<h1>Your Top Career Matches</h1>
<ul>
  {% for score, career in results %}
    <li>
      <h2>{{ career.name }}</h2>
      <p>{{ career.description }}</p>
      <p><strong>Match Score:</strong> {{ score }}</p>
    </li>
  {% endfor %}
</ul>
<a href="/">Start Over</a>
"""

if __name__ == "__main__":
    app.run(debug=False)
