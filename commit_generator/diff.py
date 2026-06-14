'''Diff acquisition module.

Retrieves the git diff as a string from stdin or subprocess,
depending on how the program is invoked.
'''

import subprocess
import sys


def get_diff(unstaged: bool = False) -> str:
    '''Acquire the `git diff` output as a string from stdin or subprocess.

    Reads from stdin if data is piped in, otherwise runs `git diff`
    via subprocess. Raises `SystemExit` if no diff is found.

    Args:
        unstaged: If `True`, retrieves unstaged changes instead of staged.

    Returns:
        The `git diff` output as a plain string.
    '''
    if not sys.stdin.isatty():
        diff = sys.stdin.read()
    else:
        flag = [] if unstaged else ['--staged']
        result = subprocess.run(
            ['git', 'diff'] + flag,
            capture_output=True,
            text=True
        )
        diff = result.stdout

    if not diff.strip():
        print('No changes detected. Stage your changes or pass a diff via stdin.')
        raise SystemExit(1)

    return diff
