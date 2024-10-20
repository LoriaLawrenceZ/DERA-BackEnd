from flask import Flask, render_template, request, Response, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep

from selecionar_persona import *

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

CORS(app, resources = {r"/chat": {"origins": "https://dera-xi.vercel.app"}})

STATUS_COMPLETED = "completed"
STATUS_REQUIRES_ACTION = "requires_action"

def der(user_prompt):
    maximum_tries = 1
    counter = 0

    while True:
        try:
            personality = personas[select_persona(user_prompt)]

            client.beta.threads.messages.create(
                thread_id = "",
                role = "user",
                content = "",
                file_ids = []
            )

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
    return jsonify({"response": der_response})

if __name__ == "__main__":
    app.run(debug = True)