This is the log of running the [`randompic.md`](../../randompic.md) prompt.



```bash
$ modal run --quiet main  --prompt randompic.md
```



<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [How the prompts work](#how-the-prompts-work)
  - [The wish prompt](#the-wish-prompt)
  - [The built in prompts](#the-built-in-prompts)
- [Prompt 1: get a list of files](#prompt-1-get-a-list-of-files)
  - [system prompt 1](#system-prompt-1)
  - [user prompt 1](#user-prompt-1)
  - [response 1:](#response-1)
- [Prompt 2: get a list of shared dependencies](#prompt-2-get-a-list-of-shared-dependencies)
  - [system prompt 2](#system-prompt-2)
  - [user prompt 2](#user-prompt-2)
  - [response 2](#response-2)
- [Prompt 3: file generation](#prompt-3-file-generation)
  - [system prompt 3a index.html](#system-prompt-3a-indexhtml)
  - [user prompt 3a](#user-prompt-3a)
  - [reponse 3a index.html](#reponse-3a-indexhtml)
  - [system prompt 3b style.css](#system-prompt-3b-stylecss)
  - [user prompt 3b](#user-prompt-3b)
  - [response 3b style.css](#response-3b-stylecss)
  - [system prompt 3c script.js](#system-prompt-3c-scriptjs)
  - [user prompt 3c](#user-prompt-3c)
  - [response 3c script.js](#response-3c-scriptjs)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->




## How the prompts work

Every ChatGPT prompt is a
[set of messages](https://platform.openai.com/docs/guides/gpt/chat-completions-api)
made up of a role and some content.
The roles are:

+ system: instructions for the model
+ user: user instructions
+ assistant: what the model generates

```js
import openai

openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)
```

### The wish prompt

The wish prompt, the description of what we want
tepiton coder tp make for us, is
pretty specific, giving it a lot of hints.
(I call it the _wish prompt_ because reasons.)

<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text"><span class="user_prompt">
A web page that displays a random picture in a pleasing layout.

- The URL to get a new random picture everytime: https://picsum.photos/400/
- You do not need to provide any query parameters
- the id of the img element is 'img'
- the id of the button is 'refresh'
- make the background tomato
- set all listeners in script.js
- set all colors in style.css
- make sure the button shows hover and clicked states
</span></code></pre>

You'll see that this prompt is repeated in every request.

### The built in prompts

- `SYSTEM_PROMPT_TO_GET_LIST_FILES`
  This prompt just asks Tepiton Coder to figure out what
  files we'll need. Its corresponding user prompt is the wish prompt.

+ `SYSTEM_PROMPT_TO_GET_SHARED_DEPENDENCIES`
  This prompt incorporates the wish prompt and the list of
  files generated to figure out dependencies.
  Its corresponding user prompt is the wish prompt.

+ `SYSTEM_PROMPT_TO_GENERATE_FILE`
  This system prompt incorporates the wish prompt,
  the list of files needed,
  and the shared dependencies to help it make sense
  of how the pieces go together.

+ `USER_PROMPT_TO_GENERATE_FILE`
  A companion user prompt, this one tells Tepiton Coder
  which file to generate, and gives lots of advice.








## Prompt 1: get a list of files


The first prompt gets a list of files needed for the program.
The system prompt is a description of what we want. We have to
be very insistent that the response is a python list of strings.


### system prompt 1
<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text">
<strong>system=>:</strong><span class="system_prompt"> You are an AI developer who is trying to write a program
that will generate code for the user based on their intent.

When given their intent, create a complete, exhaustive list of files
that the user would write to make the program.

only list the filepaths you would write, and return them as a python list of strings.
do not add any other explanation, only return a python list of strings.
It is IMPORTANT that you return ONLY a python list of strings, not a string.</span>
</code></pre>


### user prompt 1
<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text"><strong>user=>:</strong><span class="user_prompt"> A web page that displays a random picture in a pleasing layout.

- The URL to get a new random picture everytime: https://picsum.photos/400/
- You do not need to provide any query parameters
- the id of the img element is 'img'
- the id of the button is 'refresh'
- make the background tomato
- set all listeners in script.js
- set all colors in style.css
- make sure the button shows hover and clicked states</span>
</code></pre>


### response 1:
<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text">
<span class="file_list">['index.html', 'style.css', 'script.js']</span>
</code></pre>




## Prompt 2: get a list of shared dependencies

### system prompt 2

<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text"><strong>system=>:</strong><span class="system_prompt"> You are an AI developer who is trying to write a program
that will generate code for the user based on their intent.

In response to the user's prompt:

    ---
    the app is:<span class="user_prompt"> A web page that displays a random picture in a pleasing layout.

- The URL to get a new random picture everytime: https://picsum.photos/400/
- You do not need to provide any query parameters
- the id of the img element is 'img'
- the id of the button is 'refresh'
- make the background tomato
- set all listeners in script.js
- set all colors in style.css
- make sure the button shows hover and clicked states</span>

    ---

    the files we have decided to generate are: <span class="file_list">['index.html', 'style.css', 'script.js']</span>

    Now that we have a list of files, we need to understand
    what dependencies they share. Please name and briefly
    describe what is shared between the files we are
    generating, including exported variables, data schemas,
    id names of every DOM elements that javascript functions
    will use, message names, and function names. Exclusively
    focus on the names of the shared dependencies, and do
    not add any other explanation.</span>

</code></pre>

### user prompt 2
<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text"><strong>user=>:</strong><span class="user_prompt"> A web page that displays a random picture in a pleasing layout.

- The URL to get a new random picture everytime: https://picsum.photos/400/
- You do not need to provide any query parameters
- the id of the img element is 'img'
- the id of the button is 'refresh'
- make the background tomato
- set all listeners in script.js
- set all colors in style.css
- make sure the button shows hover and clicked states</span>
</code></pre>


### response 2

<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text">
<span class="shared_dependencies">Shared dependencies between the files we are generating:

- index.html:
    - img element with id 'img'
    - button element with id 'refresh'
    - script.js file
    - style.css file

- style.css:
    - background color 'tomato'
    - hover and clicked states for button with id 'refresh'

- script.js:
    - img element with id 'img'
    - button element with id 'refresh'
    - event listeners for button with id 'refresh'</span>
</code></pre>

## Prompt 3: file generation


### system prompt 3a index.html

<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text">
<strong>system=>:</strong> <span class="system_prompt">You are an AI developer who is trying to write a program
that will generate code for the user based on their intent.

the app is: <span class="user_prompt"> A web page that displays a random picture in a pleasing layout.

- The URL to get a new random picture everytime: https://picsum.photos/400/
- You do not need to provide any query parameters
- the id of the img element is 'img'
- the id of the button is 'refresh'
- make the background tomato
- set all listeners in script.js
- set all colors in style.css
- make sure the button shows hover and clicked states</span>

the files we have decided to generate are: <span class="file_list">['index.html', 'style.css', 'script.js']</span>
the shared dependencies (like filenames and variable names)
we have decided on are:
<span class="shared_dependencies">Shared dependencies between the files we are generating:

- index.html:
    - img element with id 'img'
    - button element with id 'refresh'
    - script.js file
    - style.css file

- style.css:
    - background color 'tomato'
    - hover and clicked states for button with id 'refresh'

- script.js:
    - img element with id 'img'
    - button element with id 'refresh'
    - event listeners for button with id 'refresh'</span>

only write valid code for the given filepath and file type,
and return only the code. do not add any other explanation,
only return valid code for that file type.</span>

</code></pre>

### user prompt 3a
<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text"><strong>user=>:</strong> <span class="filegen_prompt">We have broken up the program into per-file generation.
Now your job is to generate only the code for the file
index.html. Make sure to have consistent filenames if
you reference other files we are also generating.

Remember that you must obey these things:

- you are generating code for the file index.html
- do not stray from the names of the files
  and the shared dependencies we have decided on
- MOST IMPORTANT OF ALL - the purpose of our app is<span class="user_prompt"> A web page that displays a random picture in a pleasing layout.

- The URL to get a new random picture everytime: https://picsum.photos/400/
- You do not need to provide any query parameters
- the id of the img element is 'img'
- the id of the button is 'refresh'
- make the background tomato
- set all listeners in script.js
- set all colors in style.css
- make sure the button shows hover and clicked states</span>

  every line of code you generate must be valid code.
- DO NOT use code fences
- DO NOT use markdown syntax.
- Do not explain the code
- return valid code for that file type.

Begin generating the code now.</span>
</code></pre>

### reponse 3a index.html

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Random Picture Generator</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <div class="container">
      <img id="img" src="https://picsum.photos/400/">
      <button id="refresh">Refresh</button>
    </div>
    <script src="script.js"></script>
  </body>
</html>
```


### system prompt 3b style.css

<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text"><strong>system=>:</strong> <span class="system_prompt">You are an AI developer who is trying to write a program
that will generate code for the user based on their intent.

the app is:<span class="user_prompt"> A web page that displays a random picture in a pleasing layout.

- The URL to get a new random picture everytime: https://picsum.photos/400/
- You do not need to provide any query parameters
- the id of the img element is 'img'
- the id of the button is 'refresh'
- make the background tomato
- set all listeners in script.js
- set all colors in style.css
- make sure the button shows hover and clicked states</span>

the files we have decided to generate are: <span class="file_list">['index.html', 'style.css', 'script.js']</span>
the shared dependencies (like filenames and variable names)
we have decided on are:
<span class="shared_dependencies">Shared dependencies between the files we are generating:

- index.html:
    - img element with id 'img'
    - button element with id 'refresh'
    - script.js file
    - style.css file

- style.css:
    - background color 'tomato'
    - hover and clicked states for button with id 'refresh'

- script.js:
    - img element with id 'img'
    - button element with id 'refresh'
    - event listeners for button with id 'refresh'</span>

only write valid code for the given filepath and file type,
and return only the code. do not add any other explanation,
only return valid code for that file type.</span>

</code></pre>

### user prompt 3b
<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text"><strong>user=>:</strong> <span class="filegen_prompt">We have broken up the program into per-file generation.
Now your job is to generate only the code for the file
style.css. Make sure to have consistent filenames if
you reference other files we are also generating.

Remember that you must obey these things:

- you are generating code for the file style.css
- do not stray from the names of the files
  and the shared dependencies we have decided on
- MOST IMPORTANT OF ALL - the purpose of our app is<span class="user_prompt"> A web page that displays a random picture in a pleasing layout.

- The URL to get a new random picture everytime: https://picsum.photos/400/
- You do not need to provide any query parameters
- the id of the img element is 'img'
- the id of the button is 'refresh'
- make the background tomato
- set all listeners in script.js
- set all colors in style.css
- make sure the button shows hover and clicked states</span>

  every line of code you generate must be valid code.
- DO NOT use code fences
- DO NOT use markdown syntax.
- Do not explain the code
- return valid code for that file type.

Begin generating the code now.</span>
</code>
</pre>

### response 3b style.css

```css
/* style.css */

body {
  background-color: tomato;
}

#refresh {
  background-color: white;
  color: tomato;
  border: 2px solid tomato;
  border-radius: 5px;
  padding: 10px;
  cursor: pointer;
}

#refresh:hover {
  background-color: tomato;
  color: white;
}

#refresh:active {
  background-color: darkred;
  color: white;
}
```

### system prompt 3c script.js



<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text">

<strong>system=>:</strong> <span class="system_prompt">You are an AI developer who is trying to write a program
that will generate code for the user based on their intent.

the app is:<span class="user_prompt"> A web page that displays a random picture in a pleasing layout.

- The URL to get a new random picture everytime: https://picsum.photos/400/
- You do not need to provide any query parameters
- the id of the img element is 'img'
- the id of the button is 'refresh'
- make the background tomato
- set all listeners in script.js
- set all colors in style.css
- make sure the button shows hover and clicked states</span>

the files we have decided to generate are: <span class="file_list">['index.html', 'style.css', 'script.js']</span>
the shared dependencies (like filenames and variable names)
we have decided on are:
<span class="shared_dependencies">Shared dependencies between the files we are generating:

- index.html:
    - img element with id 'img'
    - button element with id 'refresh'
    - script.js file
    - style.css file

- style.css:
    - background color 'tomato'
    - hover and clicked states for button with id 'refresh'

- script.js:
    - img element with id 'img'
    - button element with id 'refresh'
    - event listeners for button with id 'refresh'</span>

only write valid code for the given filepath and file type,
and return only the code. do not add any other explanation,
only return valid code for that file type.</span>

</code></pre>

### user prompt 3c
<pre style="background-color: rgb(248, 248, 248); height: 66px;"><code class="text"><strong>user=>:</strong> <span class="filegen_prompt">We have broken up the program into per-file generation.
Now your job is to generate only the code for the file
script.js. Make sure to have consistent filenames if
you reference other files we are also generating.

Remember that you must obey these things:

- you are generating code for the file script.js
- do not stray from the names of the files
  and the shared dependencies we have decided on
- MOST IMPORTANT OF ALL - the purpose of our app is<span class="user_prompt"> A web page that displays a random picture in a pleasing layout.

- The URL to get a new random picture everytime: https://picsum.photos/400/
- You do not need to provide any query parameters
- the id of the img element is 'img'
- the id of the button is 'refresh'
- make the background tomato
- set all listeners in script.js
- set all colors in style.css
- make sure the button shows hover and clicked states</span>

  every line of code you generate must be valid code.
- DO NOT use code fences
- DO NOT use markdown syntax.
- Do not explain the code
- return valid code for that file type.

Begin generating the code now.</span>

</code></pre>


### response 3c script.js

```js
// script.js

const img = document.getElementById('img');
const refreshBtn = document.getElementById('refresh');

function getRandomImage() {
  const randomImageUrl = `https://picsum.photos/400/?random=${Math.random()}`;
  img.src = randomImageUrl;
}

refreshBtn.addEventListener('click', getRandomImage);
```

</code>
</pre>

<style>
  .user_prompt { color: blue; }
  .system_prompt { color: green; }
  .file_list { color: blue; background-color: yellow;}
  .shared_dependencies {color: purple; }
  .filegen_prompt {color: #D95E00; }
</style>

