
# tepiton coder

A program that uses the ChatGPT API to generate code.
A little bigger than Hello World, but not too much bigger.
The interesting thing is that the program uses the output of one
completion to set up the next.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [What I did](#what-i-did)
- [Using Modal](#using-modal)
- [What I learned](#what-i-learned)
- [What it does](#what-it-does)
  - [First prompt: generate a list of files](#first-prompt-generate-a-list-of-files)
  - [Second prompt: find shared dependencies](#second-prompt-find-shared-dependencies)
  - [Third prompt: generate code](#third-prompt-generate-code)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->



I was looking for an interesting project that used
the ChatGPT API and was wrtten in Python. I found
[smol-ai/developer](https://github.com/smol-ai/developer)
which is described as _the thing that builds the thing_.

> Given a prompt that describes a program in detail,
> it creates the code and writes out the files. 

I was having trouble understanding the prompts, so
I pulled them out into a separate file and reorganized
and renamed the functions. Since I was more interested
in the mechanics of writing in Python than in generating
code, I removed the files that weren't germane to my goal.

The point at which I diverged from
[smol-ai/developer](https://github.com/smol-ai/developer) 
is at the branch named `smol-ai/developer`.

## What I did

- Got rid of all the code except for [`main.py`](./main.py) 
  to concentrate on learning Python
- Got rid of the devcontainer stuff. I do want to learn
  about devcontainers, but not right now.
- Moved the prompts to [`prompts.py`](./prompts.py) so I could
  see what was going on. I gave the goofy names that made sense to me.
- Added [pretty printing(./utils.py)] code to see what was going on
- Not interested in tokens at the moment
- Refactored a bit

## Using Modal

The original used [Modal](https://modal.com),
and I had just started playing with it.
Something about using large language models requiring
a lot of ... everything. It seemed to take a little of
the pain of learning the Python ecosystem.

For what it's worth, in working
on this project I've used about $0.01 of the free tier.


## What I learned

I'm learning about LLMs and using ChatGPT seems to be a convenient
place to start. I've played with the OpenAI API in JavaScript, but
it seems like all the cool kids are using Python.

The interesting thing about this project, of course, is how
it uses the output of one completion to set up the next.
That was the main thing I wanted to learn.

Prompts are weird. A prompt that
works one day, doesn't quite work the next. 
My inclination when something doesn't work is to
make the prompt more specific, but somehow I end up
making it louder.

The [original project](https://github.com/smol-ai/developer) was
designed for GPT-4, which apparently generate the code for a Chrome
plugin. I'm using GPT-3.5 and my aims are much more modest.


I still don't like Python. Probably because I don't use it much,
I find it difficult to read. My eye keeps scanning for curly braces.
It's not clear to me when newlines are OK
and when they're not.
It's a new ecosystem where they do things differently than
in the JavaScript and Bash worlds. It is a strange and colorful place.

## What it does

This is a simple case. It generates a single file. I'll annotate
the program's output.

ChatGPT's prompts are
[role/content pairs](https://platform.openai.com/docs/guides/gpt/chat-completions-api).
Each request can have more than one element. In the output 

- `system=>:` indicates a system prompt
- `user=>:` indicates a user prompt




```bash
modal run --quiet main --prompt "a bash script that scans all the repos and lists the ones that are behind their upstream repos"
```

With [`SHOW_TRACE`](./constants.py) set to `True`, it generates this output.


### First prompt: generate a list of files

The goal is to generate a multifile program, so
the the first thing is to ask GPT to come up
with the list of files it's going to generate.

The `system` prompt sets the task, The `user` prompt
is the prompt you provide.


```text
----------------------------------------
system=>: You are an AI developer who is trying to write a program
that will generate code for the user based on their intent.

When given their intent, create a complete, exhaustive list of files
that the user would write to make the program.

only list the filepaths you would write, and return them as a python list of strings.
do not add any other explanation, only return a python list of strings.
It is IMPORTANT that you return ONLY a python list of strings, not a string.
user=>: a bash script that scans all the repos and lists the ones that are behind their upstream repos
----------------------------------------

RESPONSE:
['scan_repos.sh']
----------------------------------------
```

Getting ChatGPT to do exactly what you want is hard.


### Second prompt: find shared dependencies

Given the files needed, and what the user wants to do,
the next step is to find the shared dependencies.
With more complicated requests, this would generate
a list of things that might be affected by the program.

```text
----------------------------------------
system=>: You are an AI developer who is trying to write a program
that will generate code for the user based on their intent.

In response to the user's prompt:

    ---
    the app is: a bash script that scans all the repos and lists the ones that are behind their upstream repos
    ---

    the files we have decided to generate are: ['scan_repos.sh']

    Now that we have a list of files, we need to understand
    what dependencies they share. Please name and briefly
    describe what is shared between the files we are
    generating, including exported variables, data schemas,
    id names of every DOM elements that javascript functions
    will use, message names, and function names. Exclusively
    focus on the names of the shared dependencies, and do
    not add any other explanation.
user=>: a bash script that scans all the repos and lists the ones that are behind their upstream repos
----------------------------------------

RESPONSE:
Based on the prompt, the only file we are generating is `scan_repos.sh`. Therefore, there are no shared dependencies between files.
----------------------------------------

This one was too easy. Note that the `user` prompt is always
the prompt that you provide.
```

### Third prompt: generate code

We now have a list of files and a list of shared dependencies.
We loop through the files and generate the code for each one.

```text
----------------------------------------
system=>: You are an AI developer who is trying to write a program
that will generate code for the user based on their intent.

the app is: a bash script that scans all the repos and lists the ones that are behind their upstream repos
the files we have decided to generate are: ['scan_repos.sh']
the shared dependencies (like filenames and variable names)
we have decided on are:
Based on the prompt, the only file we are generating is `scan_repos.sh`. Therefore, there are no shared dependencies between files.

only write valid code for the given filepath and file type,
and return only the code. do not add any other explanation,
only return valid code for that file type.
user=>: We have broken up the program into per-file generation.
Now your job is to generate only the code for the file
scan_repos.sh. Make sure to have consistent filenames if
you reference other files we are also generating.

Remember that you must obey these things:

- you are generating code for the file scan_repos.sh
- do not stray from the names of the files
  and the shared dependencies we have decided on
- MOST IMPORTANT OF ALL - the purpose of our app is a bash script that scans all the repos and lists the ones that are behind their upstream repos
  every line of code you generate must be valid code.
- DO NOT use code fences 
- DO NOT use markdown syntax.
- Do not explain the code
- return valid code for that file type.

Begin generating the code now.
----------------------------------------

RESPONSE:
#!/bin/bash

# Define the upstream remote name
UPSTREAM_REMOTE="upstream"

# Loop through all the directories in the current directory
for dir in */; do
  # Change into the directory
  cd "$dir" || continue

  # Get the current branch name
  CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

  # Check if the upstream remote exists
  if ! git ls-remote --exit-code "$UPSTREAM_REMOTE" &> /dev/null; then
    echo "Upstream remote does not exist for $dir"
    cd ..
    continue
  fi

  # Fetch the upstream changes
  git fetch "$UPSTREAM_REMOTE"

  # Check if the current branch is behind the upstream branch
  if git status -uno | grep -q "Your branch is behind"; then
    echo "$dir is behind upstream branch"
  fi

  # Change back to the parent directory
  cd ..
done
----------------------------------------
```

The generated code ends up in the `generated` directory.

