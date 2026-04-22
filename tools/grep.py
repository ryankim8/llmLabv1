import glob
import re
from tools.safety import is_path_safe


def grep(pattern, path):
    """
    >>> # Normal Grep
    >>> grep('doctest', 'testCases/testV1.txt')
    'This is a doctest for the cat tool'

    >>> # No Matches
    >>> grep('nomatch', 'testCases/testV1.txt')
    ''

    >>> # Unsafe Path
    >>> grep('isThisUnsafe', '/unsafe/veryUnsafe.txt')
    'Access denied: unsafe path'

    >>> # Unsafe Path with Traversal
    >>> grep('isThisUnsafe', '../superDuperUnsafe.txt')
    'Access denied: unsafe path'

    >>> #Unreadable File
    >>> import os
    >>> with open('testCases/temp.bin', 'wb') as f:
    ...     _ = f.write(bytes([0x80, 0x81]))
    >>> grep('pattern', 'testCases/temp.bin')
    ''
    >>> os.remove('testCases/temp.bin')
    """
    if not is_path_safe(path):
        return 'Access denied: unsafe path'
    matches = []
    for filepath in sorted(glob.glob(path)):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if re.search(pattern, line):
                        matches.append(line.rstrip('\n'))
        except Exception:
            continue
    return '\n'.join(matches)


SCHEMA = {
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
}
