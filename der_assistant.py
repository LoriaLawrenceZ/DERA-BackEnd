import json
from logging import exception

from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep

from der_tools import my_tools
from select_mood import fernando
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

        with open(filename, "w", encoding = "utf-8") as file:
            json.dump(data, file, ensure_ascii = False, ident = 4)

        print ("Arquivo 'assistants.json' criado com sucesso!")

    try:
        with open(filename, "r", encoding = "utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError as fnfe:
        print("Arquivo 'assistants.json' não encontrado!")

def create_thread():
    return client.beta.threads.create()

def create_file_ids_list():
    file_ids_list = []

def create_assistant(file_ids_list):
    der_gpt4 = client.beta.assistants.create(
        name = "Der Agropesca",
        description = "Assistant that simulates the person Fernando Rheder Batista Nascimento, also known as Der Agropesca.",
        instructions = f"""
            {fernando}.
            Você não deve responder como se fosse uam pessoa estranha, mas sim um amigo!
            Além disso, acesse os arquivos associados a você e a thread para responder as perguntas para ser mais assertivo.
        """,
        model = "gpt-4",
        tools = my_tools
    )