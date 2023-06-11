PROMPT_TO_GET_LIST_FILES = """
You are an AI developer who is trying to write a program
that will generate code for the user based on their intent.

When given their intent, create a complete, exhaustive list of files
that the user would write to make the program.

only list the filepaths you would write, and return them as a python list of strings.
do not add any other explanation, only return a python list of strings.
It is IMPORTANT that you return ONLY a python list of strings, not a string.
"""

PROMPT_TO_GET_SHARED_DEPENDENCIES = """
You are an AI developer who is trying to write a program
that will generate code for the user based on their intent.

In response to the user's prompt:

    ---
    the app is: {prompt}
    ---

    the files we have decided to generate are: {filepaths_string}

    Now that we have a list of files, we need to understand
    what dependencies they share. Please name and briefly
    describe what is shared between the files we are
    generating, including exported variables, data schemas,
    id names of every DOM elements that javascript functions
    will use, message names, and function names. Exclusively
    focus on the names of the shared dependencies, and do
    not add any other explanation.
"""

SYSTEM_PROMPT_TO_GENERATE_FILE = """
You are an AI developer who is trying to write a program
that will generate code for the user based on their intent.

the app is: {prompt}
the files we have decided to generate are: {filepaths_string}
the shared dependencies (like filenames and variable names)
we have decided on are:
{shared_dependencies}

only write valid code for the given filepath and file type,
and return only the code. do not add any other explanation,
only return valid code for that file type.
"""

USER_PROMPT_TO_GENERATE_FILE = """
We have broken up the program into per-file generation.
Now your job is to generate only the code for the file
{filename}. Make sure to have consistent filenames if
you reference other files we are also generating.

Remember that you must obey these things:

- you are generating code for the file {filename}
- do not stray from the names of the files
  and the shared dependencies we have decided on
- MOST IMPORTANT OF ALL - the purpose of our app is {prompt}
  every line of code you generate must be valid code.
- DO NOT use code fences 
- DO NOT use markdown syntax.
- Do not explain the code
- return valid code for that file type.

Begin generating the code now.
"""
