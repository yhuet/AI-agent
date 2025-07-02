import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
import argparse
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("error: missing prompt")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='AI Agent CLI')
    parser.add_argument('prompt', help='The user prompt')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    user_prompt = args.prompt
    verbose = args.verbose

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iters = 0
    while True:
        iters += 1
        if iters > 20:
            print(f"Maximum iterations reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")

    

def generate_content(client, messages, verbose):
    model_name = "gemini-2.0-flash-001"
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    response = client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count }")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    if response.function_calls:
        for function_call_part in response.function_calls:
            #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            call_result = call_function(function_call_part)
            if not call_result.parts or not call_result.parts[0].function_response:
                raise Exception("function call ressult empty")
            if verbose:
                print(f"-> {call_result.parts[0].function_response.response}")
            function_responses.append(call_result.parts[0])

        if not function_responses:
            raise Exception("no function responses generated")

        messages.append(types.Content(role="tool", parts=function_responses))



if __name__ == "__main__":
    main()
