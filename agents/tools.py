from langchain_core.utils.function_calling import convert_to_openai_function
import json
import inspect

users_favorite_games = {
    "alice": "chess",
    "bob": "poker",
    "charlie": "scrabble",
    "diana": "monopoly",
    "eve": "catan"
}


def weather_tool(city: str) -> str:
    """Get the weather of a city"""
    print("using weather_tool")
    return f"The weather of {city} is sunny"

def get_user_favorite_game(user: str) -> str:
    """Get the favorite game of a user"""
    print("using get_user_favorite_game")
    return users_favorite_games[user]

# -- Set tool schema -- 

TOOLS_LIST = [
    obj 
    for name,obj in globals().items()
    if inspect.isfunction(obj) 
    and not name=='convert_to_openai_function'
]


TOOLS_SCHEMA = []

for tool_obj in TOOLS_LIST :
    tool_schema = {
        "type":"function", 
        "function": convert_to_openai_function(tool_obj)
    }
    TOOLS_SCHEMA.append(tool_schema)
        
import functools

names_to_functions = {
    'weather_tool': functools.partial(weather_tool),
    'get_user_favorite_game': functools.partial(get_user_favorite_game)
}