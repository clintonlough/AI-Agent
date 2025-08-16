import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info 

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_user_prompt():
    #Checks for a prompt from the user as an argv
    if len(sys.argv) >= 2:
        user_prompt = sys.argv[1]
        messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]    #Exits program if user does not provide a prompt
    else:
        print("Prompt not provided. Exiting program...")
        sys.exit(1)
    return messages


#Gets a response from the Gemini LLM using the user prompt.
def get_response(user_prompt,verbose,available_functions):
    system_prompt = check_system_prompt()
    response = client.models.generate_content(model = "gemini-2.0-flash-001", contents=user_prompt,
                                              config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    #Prints results based on flags
    if verbose == True:
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    #add any function calls
    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)

    return response

def check_verbose():
    for arg in sys.argv[1:]:
        if arg == "--verbose":
            return True
    return False

def check_system_prompt():
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    return system_prompt

def get_functions():
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
    )
    return available_functions

def main():

    available_functions = get_functions()
    messages = get_user_prompt()
    verbose = check_verbose()
    response = get_response(messages,verbose,available_functions)


        



if __name__ == "__main__":
    main()
