import json

from flask import Flask, render_template, request, Response, jsonify
from flask_cors import CORS, cross_origin
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep

from der_assistant import get_json
from der_tools import my_functions
from select_mood import *

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
CORS(app, resources = {r"/chat": {"origins": "*"}})

der_assistant_info = get_json()
assistant_id = der_assistant_info["assistant_id"]
thread_id = der_assistant_info["thread_id"]
file_ids = der_assistant_info["file_ids"]

STATUS_COMPLETED = "completed"
STATUS_REQUIRES_ACTION = "requires_action"

def der(user_prompt):
    maximum_tries = 1
    counter = 0

    while True:
        try:
            mood = personas[select_mood(user_prompt)]

            client.beta.threads.messages.create(
                thread_id = thread_id,
                role = "user",
                content = f"""
                    Assuma, de agora em diante, o humor/temperamento abaixo.
                    Ignore os humores/temperamentos anteriores.
                    
                    # Humor / Temperamento
                    {mood}
                """
            )
            client.beta.threads.messages.create(
                thread_id = thread_id,
                role = "user",
                content = user_prompt["text"]
            )

            run = client.beta.threads.runs.create(
                thread_id = thread_id,
                assistant_id = assistant_id
            )

            while run.status != STATUS_COMPLETED:
                run = client.beta.threads.runs.retrieve(
                    thread_id = thread_id,
                    run_id = run.id
                )

                if run.status == STATUS_REQUIRES_ACTION:
                    triggered_tool = run.required_action.submit_tool_outputs.tool_calls
                    triggered_tools_responses = []

                    for tool in triggered_tool:
                        function_name = tool.function.name
                        chosen_function = my_functions[function_name]
                        tool_arguments = json.loads(tool.function.arguments)

                        tool_response = chosen_function(tool_arguments)

                        triggered_tools_responses.append(tool_response)

                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id = thread_id,
                        run_id = run.id,
                        tool_outputs = triggered_tools_responses
                    )

            history = client.beta.threads.messages.list(thread_id = thread_id).data
            response = history[0]
            return {"content": response.content}

        except Exception as e:
            counter += 1
            if counter >= maximum_tries:
                return {"content": "Erro no GPT: %s" % e}
            print("Erro de comunicação com a OpenAI:", e)
            run = client.beta.threads.runs.cancel(
                thread_id = thread_id,
                run_id = run.id
            )
            sleep(1)

@app.route("/chat", methods=["POST"])
@cross_origin()
def chat():
    user_prompt = request.json["msg"]
    response = der(user_prompt)
    der_response = response["content"][0].text.value
    return jsonify({"response": der_response})

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)