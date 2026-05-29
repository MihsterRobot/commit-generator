import argparse

from commit_generator import diff, git, llm


def main() -> None:
    '''Entry point for the commit message generator CLI.

    Parses arguments, acquires the `git diff`, generates conventional commit
    message suggestions, and either prints them or applies one as a commit.
    '''
    parser = argparse.ArgumentParser(
        description='Generate conventional commit message suggestions from a git diff.'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Interactively select a suggestion and apply it as a git commit.'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=3,
        help='Number of suggestions to generate (default: 3).'
    )
    parser.add_argument(
        '--unstaged',
        action='store_true',
        help='Use unstaged changes instead of staged.'
    )

    args = parser.parse_args()

    diff_text = diff.get_diff(unstaged=args.unstaged)
    suggestions = llm.get_suggestions(diff_text, count=args.count)

    if args.apply:
        git.apply_suggestion(suggestions)
    else:
        print('\nSuggested commit messages:\n')
        for i, suggestion in enumerate(suggestions, start=1):
            print(f'  {i}. {suggestion}')
        print()


if __name__ == '__main__':
    main()
