from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# Define 100 questions
questions = [
    "Do you enjoy solving complex problems?",
    "Are you comfortable speaking in front of a crowd?",
    "Do you like working with your hands?",
    "Are you interested in technology?",
    "Do you enjoy helping others?",
    "Are you good at organizing things?",
    "Do you prefer working in a team?",
    "Do you enjoy creative activities like drawing or writing?",
    "Do you prefer working outdoors?",
    "Do you like working with numbers?",
    "Are you detail-oriented?",
    "Do you enjoy learning about how things work?",
    "Do you like managing people or projects?",
    "Do you enjoy teaching or mentoring others?",
    "Do you enjoy writing or storytelling?",
    "Do you enjoy caring for animals?",
    "Do you like fast-paced environments?",
    "Do you enjoy cooking or baking?",
    "Do you like working with machines?",
    "Do you enjoy scientific research?",
    "Do you like helping people in emergencies?",
    "Do you enjoy designing things?",
    "Do you enjoy traveling?",
    "Do you enjoy analyzing data?",
    "Are you good at resolving conflicts?",
    "Do you like taking the lead in group settings?",
    "Do you enjoy playing with code or scripting?",
    "Do you enjoy planning events?",
    "Do you like fixing things?",
    "Do you enjoy making decisions quickly?",
    "Do you enjoy physical activities?",
    "Are you interested in law and justice?",
    "Do you enjoy talking to new people?",
    "Do you enjoy solving math problems?",
    "Do you enjoy designing user interfaces?",
    "Do you like writing reports?",
    "Do you enjoy watching documentaries?",
    "Do you enjoy DIY home projects?",
    "Are you interested in environmental issues?",
    "Do you enjoy creating digital content?",
    "Are you comfortable using spreadsheets?",
    "Do you enjoy photography?",
    "Do you enjoy keeping things clean and organized?",
    "Do you enjoy drawing or painting?",
    "Do you enjoy competitive situations?",
    "Do you enjoy exploring new places?",
    "Do you enjoy psychology or understanding behavior?",
    "Do you enjoy historical subjects?",
    "Do you enjoy creating videos?",
    "Do you like playing strategy games?",
    "Do you enjoy gardening?",
    "Do you enjoy participating in community service?",
    "Do you enjoy working with children?",
    "Do you enjoy programming apps?",
    "Do you like managing finances?",
    "Do you enjoy interior design?",
    "Do you enjoy woodworking?",
    "Do you enjoy traveling for work?",
    "Do you like handling customer complaints?",
    "Do you enjoy analyzing financial trends?",
    "Do you enjoy giving advice to friends?",
    "Do you enjoy social media?",
    "Do you enjoy talking about fashion?",
    "Do you enjoy helping sick people?",
    "Do you enjoy teaching languages?",
    "Do you like performing on stage?",
    "Do you enjoy using editing software?",
    "Do you enjoy learning about history?",
    "Do you enjoy training others?",
    "Do you enjoy driving vehicles?",
    "Do you enjoy talking about science?",
    "Do you like organizing files?",
    "Do you like giving presentations?",
    "Do you enjoy assembling furniture?",
    "Do you enjoy mentoring students?",
    "Do you enjoy analyzing criminal cases?",
    "Do you enjoy painting houses?",
    "Do you enjoy studying biology?",
    "Do you enjoy giving tours?",
    "Do you enjoy writing code?",
    "Do you enjoy helping the elderly?",
    "Do you enjoy making spreadsheets?",
    "Do you enjoy acting in plays?",
    "Do you enjoy making crafts?",
    "Do you enjoy giving interviews?",
    "Do you enjoy learning about medicine?",
    "Do you enjoy working in hospitals?",
    "Do you like giving motivational speeches?",
    "Do you like organizing sporting events?",
    "Do you enjoy learning new languages?",
    "Do you like brainstorming new ideas?",
    "Do you enjoy selling products?",
    "Do you enjoy hosting events?",
    "Do you enjoy fixing cars?",
    "Do you like flying drones?",
    "Do you enjoy taking care of pets?",
    "Do you enjoy working late nights?",
    "Do you enjoy making music?",
    "Do you enjoy attending conferences?",
    "Do you enjoy building things?",
    "Do you enjoy solving puzzles?",
    "Do you enjoy helping small businesses?"
]

careers = [
    {"name": "Data Scientist", "traits": [0, 3, 9, 23, 33]},
    {"name": "Teacher", "traits": [4, 13, 52, 66]},
    {"name": "Mechanical Engineer", "traits": [2, 18, 28, 90]},
    {"name": "Graphic Designer", "traits": [7, 21, 43, 55]},
    {"name": "Chef", "traits": [17, 84]},
    {"name": "Software Developer", "traits": [3, 26, 53, 74]},
    {"name": "Veterinarian", "traits": [15, 61, 87]},
    {"name": "Event Planner", "traits": [27, 75, 76]},
    {"name": "Police Officer", "traits": [20, 30, 70]},
    {"name": "Marketing Manager", "traits": [33, 57, 58]},
    # Add 90 more careers with specific traits
]

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Career Chat</title>
        <style>
            body { font-family: Arial; background: #f0f0f0; padding: 20px; }
            #chat { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            .ai, .user { margin: 10px 0; padding: 10px; border-radius: 10px; }
            .ai { background: #e0f7fa; text-align: left; }
            .user { background: #dcedc8; text-align: right; }
            input { width: 100%; padding: 10px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div id="chat">
            <div class="ai">Hi! I'm your career AI. Ready to explore your future?</div>
        </div>
        <form onsubmit="sendMessage(event)">
            <input id="input" placeholder="Type your answer (yes/no)..." autocomplete="off">
        </form>
        <script>
            let qIndex = 0;
            let answers = [];
            const questions = {{ questions|tojson }};
            const chat = document.getElementById("chat");
            const input = document.getElementById("input");

            function sendMessage(e) {
                e.preventDefault();
                const text = input.value.trim();
                if (!text) return;
                chat.innerHTML += `<div class='user'>${text}</div>`;
                answers.push(text.toLowerCase().startsWith('y'));
                input.value = '';

                qIndex++;
                if (qIndex < 25 && qIndex < questions.length) {
                    setTimeout(() => {
                        chat.innerHTML += `<div class='ai'>${questions[qIndex]}</div>`;
                        window.scrollTo(0, document.body.scrollHeight);
                    }, 500);
                } else {
                    fetch('/result', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(answers)
                    }).then(res => res.json()).then(data => {
                        chat.innerHTML += `<div class='ai'>Top careers for you:</div>`;
                        data.forEach(c => chat.innerHTML += `<div class='ai'><strong>${c.name}</strong>: ${c.description || '—'}</div>`);
                        window.scrollTo(0, document.body.scrollHeight);
                    });
                }
            }

            chat.innerHTML += `<div class='ai'>${questions[0]}</div>`;
        </script>
    </body>
    </html>
    ''', questions=questions)

@app.route('/result', methods=['POST'])
def result():
    user_answers = request.get_json()
    scores = []
    for career in careers:
        match_score = sum(user_answers[i] for i in career['traits'] if i < len(user_answers))
        scores.append((match_score, career))
    scores.sort(reverse=True)
    return jsonify([c for s, c in scores[:5]])

if __name__ == '__main__':
    app.run(debug=False)
