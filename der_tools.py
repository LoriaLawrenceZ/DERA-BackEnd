from flask import Flask,render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

my_tools = [
    {"type": "file_search"},
    {
        "type": "function",
        "function": {
            "name": "procurar_verdades",
            "description": "Valide um código promocional com base nas diretrizes de Descontos e Promoções da empresa",
            "parameters": {
                "type": "object",
                "properties": {
                    "fato": {
                        "type": "string",
                        "description": "O fato em voga que está sendo analisado para ver se é verdade ou não",
                    },
                    "verdade": {
                        "type": "boolean",
                        "description": "A veracidade do fato em voga",
                    },
                },
                "required": ["codigo", "validade"],
            }
        }
    }
]

def is_it_true(arguments):
    fato = arguments.get("fato")
    verdade = arguments.get("verdade")

    return f"""
    # Formato de Resposta
    
    {fato} é {verdade}!
    """

my_functions = {
    "is_it_true": is_it_true
}