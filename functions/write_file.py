import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)

    if abs_path == abs_working_path or abs_path.startswith(abs_working_path + os.sep):
        if not os.path.isfile(abs_path):
            with open(abs_path, 'w') as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        else:
            with open(abs_path, 'w') as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    else:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    

# Schema definition (at module level, not inside any function)    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes content to a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path at which to write the specified file",
            ),
            "content": types.Schema(
            type=types.Type.STRING,
            description="the content to write to the file.",
            ),
        },
    ),
)