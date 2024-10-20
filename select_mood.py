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

def select_mood(user_message):
    system_prompt = """
    Faça uma análise da mensagem informada abaixo para identificar se o sentimento é: alegre ou triste.
    Caso não seja possível se identificar o sentimento na mensagem informada, tome como verdade o 'alegre'
    Retorne apenas as possibilidas informados como resposta.
    """

    response = client.chat.completions.create(
        model = select_model(system_prompt + user_message["text"]),
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message["text"]
            }
        ],
        temperature = 1
    )

    return response.choices[0].message.content.lower()