import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)

    if abs_path == abs_working_path or abs_path.startswith(abs_working_path + os.sep):
        if not os.path.isdir(abs_path):
            return f'Error: "{directory}" is not a directory'
        else:
            contents =  os.listdir(abs_path)
            directory_contents = ""
            for content in contents:
                name = str(content)
                temp_path = os.path.join(full_path, content)
                file_size = os.path.getsize(temp_path)
                is_dir = not os.path.isfile(temp_path)
                item_info = f"- {name}: file_size={file_size} bytes, is_dir={is_dir}"
                directory_contents += item_info + "\n"
            return directory_contents[:-1]

    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

# Schema definition (at module level, not inside any function)    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def main():
    pass

if __name__ == "__main__":
    # Your manual tests here
    print(get_files_info("calculator", "."))
