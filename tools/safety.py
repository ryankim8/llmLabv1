def is_path_safe(path):
    """
    Helper function to check if a file path is safe

    >>> is_path_safe('.')
    True
    >>> is_path_safe('tools/ls.py')
    True
    >>> is_path_safe('/no/notSafe')
    False
    >>> is_path_safe('../unsafe.txt')
    False
    >>> is_path_safe('no/../../no/unsafe')
    False
    """
    if path.startswith('/'):
        return False
    if '..' in path.split('/'):
        return False
    return True
