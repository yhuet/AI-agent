import os
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_full_path = os.path.abspath(full_path)
    if not absolute_full_path.startswith(absolute_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_path, "r") as file:
            content = file.read(10000)
            if len(content) > 9999:
                content = content[:10000] + f'\n[...File "{file_path}" truncated at 10000 characters]'
            return content
    except Exception as e:
        print(f"Error: {e}")

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Shows file content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to view content from.",
            ),
        },
    ),
)
