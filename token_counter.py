import tiktoken

model_list = [
    {
        "model": "gpt-4",
        "max_tokens": 1000
    },
    {
        "model": "gpt-3.5-turbo",
        "max_tokens": 100
    },
    {
        "model": "gpt-3.5",
        "max_tokens": 10
    }
]

def select_model(total_prompt):
    for model in model_list:
        encoder = tiktoken.encoding_for_model(model["model"])
        token_list = encoder.encode(total_prompt)
        token_ammount = len(token_list)

        if token_ammount <= model["max_tokens"]:
            return model["model"]

    return None