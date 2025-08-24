import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(full_path)
    abs_working_path = os.path.abspath(working_directory)

    if abs_path == abs_working_path or abs_path.startswith(abs_working_path + os.sep):
        if not os.path.isfile(abs_path):
            return f'Error: File "{file_path}" not found.'
        elif not str(file_path).endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        else:
            try:
                cmd = ["python3", str(abs_path)] + args
                run_process = subprocess.run(
                    cmd,
                    timeout=30, #seconds
                    capture_output= True
                )
                if run_process.returncode != 1:
                    return f"STDOUT: {run_process.stdout}, STDERR: {run_process.stderr}. Process exited with code {run_process.returncode}."
                elif run_process.stdout == None:
                    return "No output produced."
                else:
                    return f"STDOUT: {run_process.stdout}, STDERR: {run_process.stderr}"
            except Exception as e:
                return f"Error: executing Python file: {e}"
                
    else:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    

# Schema definition (at module level, not inside any function)    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file at a specified file path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to open the required file at. If the file is not a .py file, raise an error.",
            ),
        },
    ),
)