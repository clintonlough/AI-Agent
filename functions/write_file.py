import os

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
    