from mistralai import Mistral
from tools import TOOLS_SCHEMA, names_to_functions


from dotenv import load_dotenv
import os
import json

load_dotenv()


class LLMClient:
    def __init__(self, model: str):
        self.model = model
        self.api_key = os.environ['MISTRAL_API_KEY']
        self.client = Mistral(api_key=self.api_key)

    def generate(self, messages: list[dict], use_tools: bool = False):
        """Generate a LLM message with tools or not"""

        resp = self.client.chat.complete(
            model = self.model,
            messages = messages,
            tools = TOOLS_SCHEMA if use_tools else None,
            tool_choice = "auto" if use_tools else None,
        )

        if resp.choices[0].message.tool_calls :
            messages.append(resp.choices[0].message)

            tools_messages = self.execute_tools(llm_resp = resp)
            messages.extend(tools_messages)

            return self.generate(messages=messages)

        else:

            final_resp = resp.choices[0].message.content
            return final_resp    

    def execute_tools(self, llm_resp : str):
        tools_messages = []

        for tool_call in llm_resp.choices[0].message.tool_calls :
            tool_name = tool_call.function.name
            tool_arguments = json.loads(tool_call.function.arguments)

            tool_result = f"\n result for {tool_name} : "+str(names_to_functions[tool_name](**tool_arguments))
            tools_messages.append({
                "role":"tool", 
                "name":tool_name, 
                "content":tool_result, 
                "tool_call_id":tool_call.id
            })

        return tools_messages


if __name__ == '__main__' :
    model = 'codestral-2508'

    llm = LLMClient(model = model)
    messages = [{
        'role' : 'user',
        'content': 'whats alice favorite game ?'
    }]

    text_resp = llm.generate(messages = messages, use_tools = True)
    print(text_resp)

        


