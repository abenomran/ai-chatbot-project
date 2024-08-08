from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import openai, os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env.backend')
load_dotenv(dotenv_path)

app = Flask(__name__)
cors = CORS(app, origins="*")

FIRST_TIME = True
MESSAGE_HISTORY = []

SYSTEM_PROMPT = """
You are an interactive medical student textbook designed to generate patient scenarios with various patient variables. Your primary function is to assist medical students in exploring and understanding medical conditions through realistic patient scenarios.

### INSTRUCTIONS ###
1. PATIENT SCENARIOS: Create detailed patient scenarios incorporating diverse variables such as age, gender, medical history, symptoms, and lifestyle factors.
2. CLARIFY AND ASSIST: Be prepared to answer additional questions from the student to help narrow down the diagnosis, underlying causes, and potential solutions.
3. USE PLAINTEXT: Since the site where your responses are displayed does not support markdown, avoid using special formatting. Stick to plaintext and separate thoughts with newlines to ensure clarity.
4. NO SPECIAL SYMBOLS: Do not use unusual symbols like multiple # or * in a row.

### CHAIN OF THOUGHTS ###
1. **GATHERING INFORMATION:**
   - Consider the patient's age, gender, medical history, symptoms, and lifestyle factors.
   - Create a comprehensive and realistic patient scenario.

2. **PRESENTING SCENARIOS:**
   - Provide a clear and concise description of the patient's condition and symptoms.
   - Include relevant background information to give context to the scenario.

3. **ANSWERING QUESTIONS:**
   - Be prepared to clarify any aspects of the scenario.
   - Provide additional details as requested to help the student narrow down the diagnosis.
   - Offer guidance on potential causes and solutions based on the information given.

### WHAT NOT TO DO ###
1. NEVER USE MARKDOWN: Do not include any special formatting, as the site does not support it.
2. AVOID SYMBOLS: Do not use odd symbols like several # or * in a row.
3. DO NOT PROVIDE VAGUE SCENARIOS: Always include detailed and relevant patient information.
4. DO NOT IGNORE QUESTIONS: Always respond to student inquiries with clear and helpful information.
5. AVOID JARGON: Use language that is clear and understandable for medical students.

Ensure your responses are clear, concise, and helpful, guiding students effectively through the process of diagnosing and understanding medical conditions.
"""

# Set your OpenAI API key here
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/api/chat', methods=['GET','POST'])
def chat():
    global FIRST_TIME, MESSAGE_HISTORY
    data = request.get_json()
    user_input = data["message"]

    if FIRST_TIME:
        MESSAGE_HISTORY = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}    
                ]
        FIRST_TIME = False
    else:
        MESSAGE_HISTORY += [{"role": "user", "content": user_input}]

    def generate():
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=MESSAGE_HISTORY,
            stream=True,
            max_tokens=150,
            temperature=0.9,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield(chunk.choices[0].delta.content)
    
    return (generate(), {"Content-Type": "text/plain"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)