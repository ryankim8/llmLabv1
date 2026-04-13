import glob
import re
from tools.safety import is_path_safe


def grep(pattern, path):
    # Returns all lines matching pattern in files matching path

    """
    Returns newline-separated lines matching pattern in files matching path.

    >>> import os
    >>> open('grep.txt', 'w').write('hello world\\nfoo bar\\nhello again')
    31
    >>> grep('hello', 'grep.txt')
    'hello world\\nhello again'
    >>> grep('zzznomatch', 'grep.txt')
    ''
    >>> os.unlink('grep.txt')
    >>> grep('hello', '/etc/passwd')
    'Access denied: unsafe path'
    >>> grep('hello', '../nope.txt')
    'Access denied: unsafe path'
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