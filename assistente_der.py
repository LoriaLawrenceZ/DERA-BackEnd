import json

from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep

from selecionar_persona import fernando
from token_counter import select_model

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4"

def get_json():
    filename = "assistants.json"

    if not os.path.exists("dados/"+filename):
        thread_id = create_thread()
        file_ids_list = create_file_ids_list()
        assistant_id = create_assistant(file_ids_list)

        data = {
            "assistant_id": assistant_id,
            "thread_id": thread_id,
            "file_ids": file_ids_list
        }

def create_thread():
    return client.beta.threads.create()

def create_file_ids_list():
    return []

def create_assistant(file_ids_list):
    assistant = client.beta.assistants.create(
        name = "Der",
        instructions = f"""
            {fernando}.
            Você não deve responder como se fosse uam pessoa estranha, mas sim um amigo!
            Além disso, acesse os arquivos associados a você e a thread para responder as perguntas para ser mais assertivo.
        """,
        model = select_model()
    )