import json
import os
from groq import Groq
from dotenv import load_dotenv
from tools.ls import ls, SCHEMA as ls_schema
from tools.cat import cat, SCHEMA as cat_schema
from tools.grep import grep, SCHEMA as grep_schema
from tools.calculate import calculate, SCHEMA as calculate_schema
from tools.doctests import doctests, SCHEMA as doctests_schema
from tools.write_file import write_file, SCHEMA as write_file_schema
from tools.write_files import write_files, SCHEMA as write_files_schema
from tools.rm import rm, SCHEMA as rm_schema



load_dotenv()

TOOLS = [ls_schema, cat_schema, grep_schema, calculate_schema, doctests_schema, write_file_schema, write_files_schema, rm_schema]

AVAILABLE_FUNCTIONS = {
    "ls": ls,
    "cat": cat,
    "grep": grep,
    "calculate": calculate,
    "doctests": doctests,
    "write_file": write_file,
    "write_files": write_files,
    "rm": rm,
}


class Chat:
    """
    >>> chat = Chat()
    >>> isinstance(chat.send_message('my name is bob', temperature=0.0), str)
    True
    >>> isinstance(chat.send_message('what is my name?', temperature=0.0), str)
    True
    """

    client = Groq()

    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant who answers questions and executes commands for the user ni 1-3 sentences. "
                    "You have access to tools that can list files, read files, search files, and do math. "
                    "When the user asks about files or directories, always call the ls tool immediately — do not ask the user to provide output and do not say you lack access. "
                    "When the user provides output from a slash command, use that information to answer their question directly without calling any tools again."
                )
            }
        ]

    def send_message(self, message, temperature=0.8):
        """
        Sends a user message and returns the assistant's reply, calling tools as needed.

        >>> chat = Chat()
        >>> isinstance(chat.send_message('my name is bob', temperature=0.0), str)   # doctest: +ELLIPSIS
        True
        """
        self.messages.append({"role": "user", "content": message})
        for _ in range(10):
            response = self.client.chat.completions.create(
                messages=self.messages,
                model="llama-3.3-70b-versatile",
                temperature=temperature,
                tools=TOOLS,
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if not tool_calls:
                result = response_message.content
                self.messages.append({"role": "assistant", "content": result})
                return result

            self.messages.append(response_message)
            for tool_call in tool_calls:
                fn_name = tool_call.function.name
                fn = AVAILABLE_FUNCTIONS.get(fn_name)
                if fn is None:
                    continue
                fn_args = json.loads(tool_call.function.arguments)
                fn_result = fn(**fn_args)
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": fn_name,
                    "content": fn_result,
                })


def handle_slash_command(line):
    """
    Parses and executes a slash command by mapping it to the corresponding tool
    in AVAILABLE_FUNCTIONS. Returns the tool output or an error string.

    >>> handle_slash_command('/ls testCases')
    'testCases/a.txt testCases/b.txt testCases/testV1.txt testCases/test_write.txt'
    >>> handle_slash_command('/cat testCases/testV1.txt')
    'This is a doctest for the cat tool'
    >>> handle_slash_command('/grep doctest testCases/testV1.txt')
    'This is a doctest for the cat tool'
    >>> handle_slash_command('/calculate 2 + 2')
    '4'
    >>> handle_slash_command('/calculate')
    'Error: calculate requires an expression'
    >>> handle_slash_command('/cat')
    'Error: cat requires a file argument'
    >>> handle_slash_command('/grep hello')
    'Error: grep requires a pattern and a path'
    >>> 'chat.py' in handle_slash_command('/ls')
    True
    >>> handle_slash_command('/unknownCmd')
    'Unknown command: unknownCmd'
    """
    parts = line[1:].split()
    command = parts[0]
    args = parts[1:]

    if command not in AVAILABLE_FUNCTIONS:
        return f'Unknown command: {command}'

    if command == 'cat' and not args:
        return 'Error: cat requires a file argument'
    if command == 'grep' and len(args) < 2:
        return 'Error: grep requires a pattern and a path'
    if command == 'calculate' and not args:
        return 'Error: calculate requires an expression'

    if command == 'calculate':
        return AVAILABLE_FUNCTIONS[command](' '.join(args))
    return AVAILABLE_FUNCTIONS[command](*args) if args else AVAILABLE_FUNCTIONS[command]()


def repl():
    """
    Starts an interactive chat loop. Checks for a .git folder and loads AGENTS.md
    if present. Slash commands are executed directly as tools and their output is
    injected into the conversation history. All other input is sent to the LLM.
    Exit with Ctrl+C or Ctrl+D.

    >>> def monkey_input(prompt, user_inputs=['/ls testCases', 'Hello, I am monkey.', 'Goodbye.']):
    ...     try:
    ...         user_input = user_inputs.pop(0)
    ...         print(f'{prompt}{user_input}')
    ...         return user_input
    ...     except IndexError:
    ...         raise KeyboardInterrupt
    >>> import builtins
    >>> builtins.input = monkey_input
    >>> result = repl()
    chat> /ls testCases
    testCases/a.txt testCases/b.txt testCases/testV1.txt testCases/test_write.txt
    chat> Hello, I am monkey.
    Hello Monkey, how can I assist you today?
    chat> Goodbye.
    Goodbye Monkey.
    <BLANKLINE>
    """
    if not os.path.exists('.git'):
        print('Error: not a git repository')
        return

    chat = Chat()

    if os.path.exists('AGENTS.md'):
        agents_content = cat('AGENTS.md')
        chat.messages.append({
            'role': 'user',
            'content': f'AGENTS.md: {agents_content}',
        })

    try:
        while True:
            user_input = input('chat> ')
            if user_input.startswith('/'):
                output = handle_slash_command(user_input)
                print(output)
                chat.messages.append({
                    "role": "user",
                    "content": f"/{user_input[1:].split()[0]} output: {output}",
                    })
            else:
                print(chat.send_message(user_input, temperature=0.0))
    except (KeyboardInterrupt, EOFError):
        print()

if __name__ == '__main__':
    repl()