from llm_client import LLMClient


model = "codestral-2508"
llm = LLMClient(model=model)

messages = [{
    'role' : 'assistant',
    'content': 'I am your assistant, how can I help ? [EXIT] for exit\n'
}]

def main():
    usr_input : str = input('I am your assistant, how can I help ? [EXIT] for exit\n')

    while usr_input != '[EXIT]':
        
        usr_message = {
            'role':'user',
            'content': usr_input
        }

        messages.append(usr_message)

        llm_resp = llm.generate(messages=messages, use_tools=True)

        usr_input=input(llm_resp+ '[EXIT] for exit\n')

        messages.append({
            'role':'assistant',
            'content' : llm_resp
        })

if __name__ == '__main__':
    main()