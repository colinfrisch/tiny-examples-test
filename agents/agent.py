from tools import TOOLS_SCHEMA, names_to_functions
from mistralai import Mistral
from dotenv import load_dotenv
import os, json

load_dotenv()
api_key = os.environ['MISTRAL_API_KEY']
model = "mistral-large-latest"
client = Mistral(api_key = api_key)

print(json.dumps(TOOLS_SCHEMA, indent = 4))

messages = [{
    'role' : 'assistant',
    'content': 'I am your assistant, how can I help ? [EXIT] for exit\n'
}]

usr_input : str = input('I am your assistant, how can I help ? [EXIT] for exit\n')

while usr_input != '[EXIT]':
    
    usr_message = {
        'role':'user',
        'content': usr_input
    }

    messages.append(usr_message)


    chat_response = client.chat.complete(
        model = model,
        messages = messages,
        tools = TOOLS_SCHEMA,
        tool_choice = "any",

    )

    llm_resp = chat_response.choices[0].message.content

    print(chat_response)

    usr_input=input(llm_resp+ '[EXIT] for exit\n')

    messages.append({
        'role':'assistant',
        'content' : llm_resp
    })

