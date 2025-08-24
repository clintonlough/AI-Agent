import os
from google.genai import types
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)

    if abs_path == abs_working_path or abs_path.startswith(abs_working_path + os.sep):
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(abs_path, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                truncated = f.read(1) != ""  # Try reading one more char to see if there's more
            if truncated == True:
                file_content_string += "\n" + f"[...File {file_path} truncated at 10000 characters]"
            return file_content_string
    else:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

# Schema definition (at module level, not inside any function)    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file contents from the specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to open the file at.",
            ),
        },
    ),
)


def main():
    pass

if __name__ == "__main__":
    # Your manual tests here
    print(get_files_info("calculator", "."))
