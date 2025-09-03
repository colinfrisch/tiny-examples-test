import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)




messages = [
    {
        "role": "user",
        "content": "Hello! Can you help me with some questions about food?"
    },
    {
        "role": "assistant", 
        "content": "Of course! I'd be happy to help you with any food-related questions you have."
    },
    {
        "role": "user",
        "content": "What's your favorite type of cuisine?"
    },
    {
        "role": "assistant",
        "content": "I enjoy discussing various cuisines! French cuisine is particularly renowned for its techniques and ingredients."
    },
    {
        "role": "user",
        "content": "What was my previous question ?",
    }
]



chat_response = client.chat.complete(
    model= model,
    messages = messages
)
print(chat_response.choices[0].message.content)