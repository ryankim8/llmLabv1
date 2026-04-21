import os
import glob
import git
from tools.safety import is_path_safe


def rm(path):
    """
    Deletes files matching the given path or glob and commits the removal.

    >>> open('testCases/tempRm.txt', 'w').close()
    >>> rm('testCases/tempRm.txt')
    'Removed and committed: testCases/tempRm.txt'
    >>> os.path.exists('testCases/tempRm.txt')
    False
    >>> rm('/unsafe/veryunsafe.txt')
    'Access denied: unsafe path'
    >>> rm('../unsafe.txt')
    'Access denied: unsafe path'
    >>> rm('testCases/random.txt')
    'No files found: testCases/random.txt'
    """
    if not is_path_safe(path):
        return 'Access denied: unsafe path'

    matches = glob.glob(path)
    if not matches:
        return f'No files found: {path}'

    for filepath in matches:
        os.remove(filepath)

    repo = git.Repo('.')
    repo.index.remove(matches, working_tree=True)
    repo.index.commit(f'[docchat] rm {path}')

    return 'Removed and committed: ' + ', '.join(matches)


SCHEMA = {
    "type": "function",
    "function": {
        "name": "rm",
        "description": "Delete files matching a path or glob and commit the removal.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path or glob to delete."}
            },
            "required": ["path"],
        },
    },
}