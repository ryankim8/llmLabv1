import glob
from tools.safety import is_path_safe


def ls(path='.'):
    # List files in directory

    """
    Returns a sorted space-separated string of filenames in the given directory.

    >>> ls()
    './README.md ./__pycache__ ./chat.py ./dist ./pyproject.toml ./requirements.txt ./tools ./venv'

    >>> ls('tools')
    'tools/__pycache__ tools/calculate.py tools/cat.py tools/grep.py tools/ls.py tools/safety.py'

    >>> ls('/etc')
    'Access denied: unsafe path'

    >>> ls('../outside')
    'Access denied: unsafe path'
    """
    if not is_path_safe(path):
        return 'Access denied: unsafe path'
    names = sorted(f.replace('\\', '/') for f in glob.glob(f'{path}/*'))
    return ' '.join(names)
