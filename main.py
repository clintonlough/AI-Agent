import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info 
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

# Get API key for Gemini
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
def get_response(messages,verbose,available_functions):
    system_prompt = check_system_prompt()
    response = client.models.generate_content(model = "gemini-2.0-flash-001", contents=messages,
                                              config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))

    #Prints results based on flags
    if verbose == True:
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    #add any function calls
    function_result = None
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_result = call_function(function_call_part, verbose)
            # Access the correct key in the response
            result = function_result.parts[0].function_response.response["result"]
            if result:
                if verbose:
                    print(f"-> {result}")
            else:
                raise Exception("Fatal error: No result from function call")
    else:
        # print(response.text)
        pass


    return response, function_result

#Checks for the verbose flag and returns true for use in other functions
def check_verbose():
    for arg in sys.argv[1:]:
        if arg == "--verbose":
            return True
    return False

#Sets the default system prompt that overrides user provided prompts and sets default behaviours
def check_system_prompt():
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

    If you don't know which file contains the needed information, first use 'get_files_info' to list the available files and directories, then proceed based on what you discover.
    Never ask the user for file or directory names; instead, use your available tools to find them.

    If you are asked to fix a bug, read .py file contents until you find the likely issue and then make the correction to the code in the file. Leave a comment at the bottom of the modified file saying what was changed prefixed by "BUGFIX:". provide a summary of the change in your response as well.
    """
    return system_prompt

#Gets the available function schemas from their separate files
def get_functions():
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
    )
    return available_functions

#handles the abstract task of calling functions
def call_function(function_call_part, verbose=False):
    #Creates a dictionary of the available functions
    function_map = {
        "get_files_info": get_files_info,        
        "get_file_content": get_file_content,    
        "write_file": write_file, 
        "run_python_file": run_python_file                
    }

    name = function_call_part.name
    args = function_call_part.args
    args["working_directory"] = "./calculator"

    if verbose:
       print(f"Calling function: {name}({args})") 
    else:
        print(f" - Calling function: {name}")

    result = function_map[name](**args)
    
    if name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"result": result},
                )
            ],
        )

#iterates through a response candidates and adds them to the messages list and then adds the function result
def update_message(messages,response,function_result):
    for candidate in response.candidates:
        messages.append(candidate.content)

    if function_result is not None:
        messages.append(function_result)

    return messages

def run_conversation(messages, verbose, available_functions):
    for i in range(20):
        try:
            response, function_result = get_response(messages, verbose, available_functions)
            messages = update_message(messages, response, function_result)
            
            # Only print the final full answer (not plans, not when there's a function call)
            if not response.function_calls and response.text:
                print("Final response:")
                print(response.text)
                break

        except Exception as e:
            handle_error(e)
            break

def handle_error(e):
    raise Exception(f"an error has occured: {e}")

def final_response(response):
    if response.text:
        return True
    return False

def main():

    available_functions = get_functions()
    messages = get_user_prompt()
    verbose = check_verbose()
    run_conversation(messages,verbose,available_functions)


        



if __name__ == "__main__":
    main()
