import os
import modal
import ast
from utils import clean_dir, trace, prettyMessages
from constants import DEFAULT_DIR, DEFAULT_MODEL, DEFAULT_MAX_TOKENS, SEPARATOR
from prompts import SYSTEM_PROMPT_TO_GET_LIST_FILES, \
                    SYSTEM_PROMPT_TO_GET_SHARED_DEPENDENCIES, \
                    SYSTEM_PROMPT_TO_GENERATE_FILE, \
                    USER_PROMPT_TO_GENERATE_FILE

stub = modal.Stub("tepiton-coder-v1")
openai_image = modal.Image.debian_slim().pip_install("openai")

@stub.function(
    image=openai_image,
    secret=modal.Secret.from_dotenv(),
    retries=modal.Retries(
        max_retries=5,
        backoff_coefficient=2.0,
        initial_delay=1.0,
    ),
    concurrency_limit=5,
    timeout=120,
)
def generate_response(model, system_prompt, user_prompt, *args):
    import openai

    openai.api_key = os.environ["OPENAI_API_KEY"]

    messages = []
    messages.append({"role": "system", "content": system_prompt.strip()})
    messages.append({"role": "user", "content": user_prompt.strip()})

    role = "assistant"
    for value in args:
        messages.append({"role": role, "content": value})
        role = "user" if role == "assistant" else "assistant"

    params = {
        "model": model,
        "messages": messages,
        "max_tokens": DEFAULT_MAX_TOKENS,
        "temperature": 0,
    }

    trace(prettyMessages(messages))
    response = openai.ChatCompletion.create(**params)
    trace(f"""RESPONSE:\n{response.choices[0]["message"]["content"]}\n{SEPARATOR}\n""")

    reply = response.choices[0]["message"]["content"]
    return reply

@stub.function()
def write_file(filename: str, filecode: str, directory: str) -> None:
    # Create the full file path
    file_path = os.path.join(directory, filename)
    trace(f"Writing file to {file_path}")
    # Create the directory if it doesn't exist
    dir = os.path.dirname(file_path)
    os.makedirs(dir, exist_ok=True)

    # Check if the file path is actually a directory
    if os.path.isdir(file_path):
        print(f"Error: {filename} is a directory, not a file.")
        return

    # Open the file in write mode and write the content to it
    with open(file_path, "w") as file:
        file.write(filecode)

def get_list_of_files_needed(model, prompt):
    """
    The first prompt (SYSTEM_PROMPT_TO_GET_LIST_FILES) gets
    a list of files needed to generate the code
    """
    file_list = []
    file_string = generate_response.call(model, SYSTEM_PROMPT_TO_GET_LIST_FILES, prompt)

    try:
        file_list = ast.literal_eval(file_string)
    except ValueError:
        print("Failed to parse result")

    return file_string, file_list

@stub.function()
def get_shared_dependencies(model, prompt, filepaths_string, directory=DEFAULT_DIR):
    """
    The second prompt (SYSTEM_PROMPT_TO_GET_SHARED_DEPENDENCIES) gets a list
    of shared dependncies, meaning things that are needed by multiple files
    """
    if os.path.exists("shared_dependencies.md"):
        with open("shared_dependencies.md", "r") as shared_dependencies_file:
            shared_dependencies = shared_dependencies_file.read()
    else:
        shared_dependencies = generate_response.call(model, SYSTEM_PROMPT_TO_GET_SHARED_DEPENDENCIES.format(prompt=prompt, filepaths_string=filepaths_string), prompt)
        write_file.call("shared_dependencies.md", shared_dependencies, directory)

    return shared_dependencies

@stub.function()
def generate_file(filename, model=DEFAULT_MODEL, filepaths_string=None, shared_dependencies=None, prompt=None):
    """
    The third prompt (SYSTEM_PROMPT_TO_GENERATE_FILE) generates the code.
    For each of the files we got from the first prompt, we generate the code
    """

    filecode = generate_response.call(model,
        SYSTEM_PROMPT_TO_GENERATE_FILE.format(prompt=prompt,
                                              filepaths_string=filepaths_string,
                                              shared_dependencies=shared_dependencies),
        USER_PROMPT_TO_GENERATE_FILE.format(filename=filename, prompt=prompt))

    return filename, filecode

@stub.local_entrypoint()
def main(prompt, directory=DEFAULT_DIR, model=DEFAULT_MODEL, file=None):

    if prompt.endswith(".md"):
        with open(prompt, "r") as promptfile:
            prompt = promptfile.read()

    clean_dir(directory)

    #    Prompt 1: Get list of files needed
    filepaths_string,list_actual = get_list_of_files_needed(model, prompt)
    #   Prompt 2: Get shared dependencies
    shared_dependencies = get_shared_dependencies(model, prompt, filepaths_string)
    #   Prompt 3: Generate code for each file
    for filename, filecode in generate_file.map(list_actual, order_outputs=False,
                                                kwargs=dict(model=model,
                                                            filepaths_string=filepaths_string,
                                                            shared_dependencies=shared_dependencies,
                                                            prompt=prompt)):
        write_file(filename, filecode, directory)

