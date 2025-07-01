import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_full_path = os.path.abspath(full_path)
    if not absolute_full_path.startswith(absolute_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    try:
        if not os.path.exists(file_path):
            dir_name = os.path.dirname(file_path)
            if dir_name:
                os.makedirs(dir_name)
        with open(file_path, "w") as file:
            bytes = file.write(content)
            if bytes:
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print(f"Error: {e}")

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write content to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write in the file.",
            ),
        },
    ),
)
