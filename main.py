import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
def get_response(user_prompt,verbose):
    response = client.models.generate_content(model = "gemini-2.0-flash-001", contents=user_prompt )

    #Prints results based on flags
    if verbose == True:
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print (response.text)

    return response

def check_verbose():
    for arg in sys.argv[1:]:
        if arg == "--verbose":
            return True
    return False


def main():

    messages = get_user_prompt()
    verbose = check_verbose()
    response = get_response(messages,verbose)


        



if __name__ == "__main__":
    main()
