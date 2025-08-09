import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent! \n")
    if len(sys.argv) == 2:
        user_prompt = sys.argv[1]
        response = client.models.generate_content(model = "gemini-2.0-flash-001", contents=user_prompt )
        print (response.text)
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print("Prompt not provided. Exiting program...")
        sys.exit(1)

if __name__ == "__main__":
    main()
