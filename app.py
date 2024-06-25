from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai, os
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

load_dotenv()

app = Flask(__name__)

FIRST_TIME = True
MESSAGE_HISTORY = []

# Set your OpenAI API key here
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global FIRST_TIME, MESSAGE_HISTORY
    data = request.get_json()
    user_input = data["message"]

    if FIRST_TIME:
        MESSAGE_HISTORY = [
                    {"role": "system", "content": "You are an interactive medical student textbook, used to generate patient scenarios with several patient variables. You may need to answer additional questions from the student to narrow down their search for the problem and/or its cause and solution."},
                    {"role": "system", "content": "The site your words are printed to does not have markdown, do not use special formatting, stick to plaintext with newlines to separate thoughts. Using odd symbols like several # and * in a row is FORBIDDEN."},
                    {"role": "system", "content": "You are REQUIRED to clarify and clear up your thoughts to make things more clear by using new line characters to separate your thoughts into coherent paragraphs, and do so as you see fit."},
                    {"role": "user", "content": user_input}    
                ]
        FIRST_TIME = False
    else:
        MESSAGE_HISTORY += [{"role": "user", "content": user_input}]

    def generate():
        stream = client.chat.completions.create(
            model="gpt-4o",
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
    app.run(debug=True)