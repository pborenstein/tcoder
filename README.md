
# tepiton coder

A program that uses the ChatGPT API to generate code.
A little bigger than Hello World, but not too much bigger.
The interesting thing is that the program uses the output of one
completion to set up the next.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [What I did](#what-i-did)
- [Using Modal](#using-modal)
- [What it does](#what-it-does)
  - [First prompt: generate a list of files](#first-prompt-generate-a-list-of-files)
  - [Second prompt: find shared dependencies](#second-prompt-find-shared-dependencies)
  - [Third prompt: generate code](#third-prompt-generate-code)
- [What I learned](#what-i-learned)

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
It seemed to take a little of
the pain of learning the Python ecosystem.
Using it feels like when I started using Git.
I'd just use the commands as incantations, without
really understanding what was going on.
That's where I am with Modal now. All that `stub.function()`
stuff is just magic to me. I hope I'm using right. but :shrug:.

For what it's worth, in working
on this project I've used about $0.01 of the free tier.


## What it does


### First prompt: generate a list of files

The goal is to generate a multifile program, so
the the first thing is to ask GPT to come up
with the list of files it's going to generate.

The `system` prompt sets the task, The `user` prompt
is the prompt you provide.

### Second prompt: find shared dependencies

Given the files needed, and what the user wants to do,
the next step is to find the shared dependencies.
With more complicated requests, this would generate
a list of things that might be affected by the program.


### Third prompt: generate code

We now have a list of files and a list of shared dependencies.
We loop through the files and generate the code for each one.

The generated code ends up in the `generated` directory.


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
