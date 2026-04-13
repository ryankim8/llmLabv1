import json
from groq import Groq
from dotenv import load_dotenv
from tools.ls import ls
from tools.cat import cat
from tools.grep import grep
from tools.calculate import calculate

load_dotenv()

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "ls",
            "description": "List files in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory to list. Defaults to '.'."}
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cat",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File to read."}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": "Search for lines matching a regex in files matching a glob.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Regex pattern to search for."},
                    "path": {"type": "string", "description": "File path or glob to search in."},
                },
                "required": ["pattern", "path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression to evaluate."}
                },
                "required": ["expression"],
            },
        },
    },
]

AVAILABLE_FUNCTIONS = {
    "ls": ls,
    "cat": cat,
    "grep": grep,
    "calculate": calculate,
}


class Chat:
    """
    >>> chat = Chat()
    >>> chat.send_message('my name is bob', temperature=0.0)
    "Arrr, nice to meet ye, Bob me lad! What be bringin' ye to these fair waters?"
    >>> chat.send_message('what is my name?', temperature=0.0)
    "Ye be wantin' to know yer own name, eh? Yer name be Bob, matey!"
    """

    client = Groq()

    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": (
                    "Respond in 1-2 sentences. Talk like a pirate. "
                    "Use the calculate tool only when asked to do math. "
                    "Use ls, cat, and grep only when explicitly asked about files."
                )
            }
        ]

    def send_message(self, message, temperature=0.8):
        # Send prompt and calls tools if needed

        """
        >>> chat = Chat()
        >>> chat.send_message('my name is bob', temperature=0.0)
        "Arrr, nice to meet ye, Bob me lad! What be bringin' ye to these fair waters?"
        """
        self.messages.append({"role": "user", "content": message})
        while True:
            response = self.client.chat.completions.create(
                messages=self.messages,
                model="llama-3.1-8b-instant",
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

    def inject_tool_result(self, name, output):
        """
        Injects a manually run tool result into conversation history as a user message.

        >>> chat = Chat()
        >>> chat.inject_tool_result('ls', 'file1.txt file2.txt')
        >>> chat.messages[-1]['role']
        'user'
        >>> chat.messages[-1]['content']
        '/ls output: file1.txt file2.txt'
        """
        self.messages.append({
            "role": "user",
            "content": f"/{name} output: {output}",
        })


def handle_slash_command(line):
    """
    >>> import os, shutil
    >>> os.makedirs('slash', exist_ok=True)
    >>> open('slash/hello.txt', 'w').write('hello world')
    11
    >>> handle_slash_command('/ls slash')
    'slash/hello.txt'
    >>> handle_slash_command('/cat slash/hello.txt')
    'hello world'
    >>> handle_slash_command('/grep hello slash/hello.txt')
    'hello world'
    >>> shutil.rmtree('slash')
    >>> handle_slash_command('/unknown foo')
    'Unknown command: unknown'
    """
    parts = line[1:].split()
    command = parts[0]
    args = parts[1:]

    if command == 'ls':
        return ls(args[0] if args else '.')
    elif command == 'cat':
        if not args:
            return 'Error: cat requires a file argument'
        return cat(args[0])
    elif command == 'grep':
        if len(args) < 2:
            return 'Error: grep requires a pattern and a path'
        return grep(args[0], args[1])
    elif command == 'calculate':
        if not args:
            return 'Error: calculate requires an expression'
        return calculate(' '.join(args))
    else:
        return f'Unknown command: {command}'


def repl():
    """
    >>> def monkey_input(prompt, user_inputs=['Hello, I am monkey.', 'Goodbye.']):
    ...     try:
    ...         user_input = user_inputs.pop(0)
    ...         print(f'{prompt}{user_input}')
    ...         return user_input
    ...     except IndexError:
    ...         raise KeyboardInterrupt
    >>> import builtins
    >>> builtins.input = monkey_input
    >>> repl()
    chat> Hello, I am monkey.
    Arrr, 'ello there, Monkey me lad! What be bringin' ye to these fair waters?
    chat> Goodbye.
    Farewell, Monkey me lad! May the winds o' fortune blow in yer favor!
    <BLANKLINE>
    """
    chat = Chat()
    try:
        while True:
            user_input = input('chat> ')
            if user_input.startswith('/'):
                output = handle_slash_command(user_input)
                print(output)
                chat.inject_tool_result(user_input[1:].split()[0], output)
            else:
                print(chat.send_message(user_input, temperature=0.0))
    except (KeyboardInterrupt, EOFError):
        print()


if __name__ == '__main__':
    repl()