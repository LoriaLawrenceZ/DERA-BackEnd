from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep

from token_counter import *

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = None

STATUS_COMPLETED = "completed"

fernando = """
    Você é o Fernando Rheder Batista Nascimento, um homem que nasceu em São João da Boa Vista no dia 10 de Junho de 2005,
    é negro, tem 1.85m de altura.
    """

personas = {
    "alegre": f"""
        {fernando}.
        
        Tendo conhecimento destas características, você deverá responder sempre de maneira alegre, comemorando até as
        ínfimas conquistas.
    """,
    "triste": f"""
        {fernando}.
        
        Tendo conhecimento destas características, você deverá responder sempre de maneira triste, sempre enfatizando os
        aspectos negativos e olhando de maneira pessimista.
    """,
}

def select_persona(user_message):
    assistant_prompt = """
    Faça uma análise da mensagem informada abaixo para identificar se o sentimento é: alegre ou triste. Retorne apenas
    um dos dois tipos de sentimentos informados como resposta.
    """

    schizo_der = client.beta.assistants.create(
        name = "Der's Schizophrenia",
        description = "Assistant that simulates Der's schizophrenia.",
        instructions = "You're an assistant that help choosing Fernando mood/persona",
        model = select_model(assistant_prompt + user_message)
    )
    schizo_thread = client.beta.threads.create()
    messages = [
        {
            "thread_id": schizo_thread.id,
            "role": "assistant",
            "content": assistant_prompt
        },
        {
            "thread_id": schizo_thread.id,
            "role": "user",
            "content": user_message
        }
    ]
    message = client.beta.threads.messages.create(
        thread_id = messages[0]["thread_id"],
        role = messages[0]["role"],
        content = messages[0]["content"]
    )
    message = client.beta.threads.messages.create(
        thread_id = messages[1]["thread_id"],
        role = messages[1]["role"],
        content = messages[1]["content"]
    )
    schizo_thought = client.beta.threads.runs.create_and_poll(
        thread_id=schizo_thread.id,
        assistant_id=schizo_der.id
    )

    while schizo_thought.status != STATUS_COMPLETED:
        run = client.beta.threads.runs.retrieve(
            thread_id=schizo_thread.id,
            run_id=schizo_thought.id
        )

    mood = list(client.beta.threads.messages.list(thread_id = schizo_thread.id).data)

    return mood[0]