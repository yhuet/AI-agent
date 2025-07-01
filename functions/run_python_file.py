import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_full_path = os.path.abspath(full_path)
    if not absolute_full_path.startswith(absolute_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path[-3:] == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        commands = ["python3", absolute_full_path]
        completed_process = subprocess.run(
            commands,
            text=True,
            timeout=30,
            capture_output=True,
            cwd=absolute_working_directory,
        )
        lines = []
        if completed_process.stdout:
            lines.append(f"STDOUT: {completed_process.stdout}")
        if completed_process.stderr:
            lines.append(f"STDERR: {completed_process.stderr}")
        if completed_process.returncode != 0:
            lines.append(f"Process exited with code {completed_process.returncode}")
        if not lines:
             lines.append("No output produced")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to run with Python.",
            ),
        },
    ),
)
