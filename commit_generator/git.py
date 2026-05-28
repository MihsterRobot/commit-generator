import subprocess


def apply_suggestion(suggestions: list[str]) -> None:
    '''Prompt the user to select a suggestion and apply it as a git commit.

    Displays a numbered list of suggestions, prompts the user to pick one,
    and runs `git commit -m` with the selected message.

    Args:
        suggestions: A list of conventional commit message strings.
    '''
    print('\nSelect a suggestion to commit:\n')
    for i, suggestion in enumerate(suggestions, start=1):
        print(f'  {i}. {suggestion}')

    print()
    user_input = input(f'Enter a number (1-{len(suggestions)}): ').strip()

    if not user_input.isdigit():
        print('Invalid input. Aborting.')
        raise SystemExit(1)

    choice = int(user_input)
    if not 1 <= choice <= len(suggestions):
        print(f'Out of range. Aborting.')
        raise SystemExit(1)

    selected = suggestions[choice - 1]

    result = subprocess.run(['git', 'commit', '-m', selected])

    if result.returncode != 0:
        print('git commit failed.')
        raise SystemExit(result.returncode)
    