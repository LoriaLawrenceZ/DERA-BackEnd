from flask import Flask, render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

STATUS_COMPLETED = "completed"
STATUS_REQUIRES_ACTION = "requires_action"

def der(user_prompt):
    maximum_tries = 1
    counter = 0

    while True:
        try:
            personality = personas[select_persona(user_prompt)]
        except Exception as e:
            counter += 1
            if counter >= maximum_tries:
                return "Erro no GPT: %s" % e
            print("Erro de comunicação com a OpenAI:", e)
            sleep(1)

@app.route("/chat", methods=["POST"])
def chat():
    user_prompt = request.json["msg"]
    response = der(user_prompt)
    der_response = response.content[0].text.value

if __name__ == "__main__":
    app.run(debug = True)