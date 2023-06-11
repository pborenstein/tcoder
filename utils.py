import os
import json
from constants import EXTENSION_TO_SKIP, SHOW_TRACE, SEPARATOR

def clean_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    else:
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                _, extension = os.path.splitext(filename)
                if extension not in EXTENSION_TO_SKIP:
                    os.remove(os.path.join(dirpath, filename))

def prettyJSON(obj):
    return json.dumps(obj, indent=4, sort_keys=True)

def trace(*args):
    if SHOW_TRACE:
        print(*args)


def prettyMessages(messages):
    s = SEPARATOR
    for m in messages:
        s += f"""{m['role']}=>: {m['content']}\n"""

    return f"""{s.strip()}\n{SEPARATOR}"""