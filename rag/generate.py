import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "codestral-2508	"

client = Mistral(api_key=api_key)

def generate(text : str) -> str:
    """
    Generate a response from the model
    """

    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": text,
            },
        ]
    )

    return chat_response.choices[0].message.content