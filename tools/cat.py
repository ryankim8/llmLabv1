from tools.safety import is_path_safe


def cat(path):
    # Reads and returns content of file

    """
    >>> import os
    >>> open('_tmp_cat.txt', 'w').write('hello world')
    11
    >>> cat('_tmp_cat.txt')
    'hello world'
    >>> os.unlink('_tmp_cat.txt')
    >>> cat('nonexistent_file.txt')
    'Error: file not found'
    >>> cat('/etc/passwd')
    'Access denied: unsafe path'
    >>> cat('../nope.txt')
    'Access denied: unsafe path'
    >>> cat('catTestv1.txt')
    'This is a doctest for the cat tool'
    """
    if not is_path_safe(path):
        return 'Access denied: unsafe path'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return 'Error: file not found'
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='utf-16') as f:
                return f.read()
        except Exception:
            return 'Error: could not decode file'
