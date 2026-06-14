'''LLM interaction module.

Sends the git diff to the Anthropic API and parses the response
into a list of conventional commit message suggestions.
'''

import anthropic
from anthropic.types import TextBlock
from dotenv import load_dotenv

load_dotenv()

MAX_DIFF_CHARS = 8000


def get_suggestions(diff: str, count: int = 3) -> list[str]:
    '''Generate conventional commit message suggestions from a `git diff`.

    Sends the diff to the Anthropic API and returns a list of suggested
    commit messages in conventional commit format.

    Args:
        diff: The `git diff` output string to generate suggestions from.
        count: The number of suggestions to generate.

    Returns:
        A list of conventional commit message strings.
    '''
    if len(diff) > MAX_DIFF_CHARS:
        diff = diff[:MAX_DIFF_CHARS] + '\n... [diff truncated]'

    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=(
            'You are an expert developer. Generate exactly {count} conventional commit message '
            'suggestions for the given git diff. Output only a numbered list, one per line, '
            'with no explanation or preamble. Follow the format: '
            'type(scope): description'
        ).format(count=count),
        messages=[
            {'role': 'user', 'content': f'Git diff:\n\n{diff}'}
        ]
    )

    response_text = next(
        block.text for block in message.content
        if isinstance(block, TextBlock)
    )
    suggestions = [
        line.split('. ', 1)[1].strip()
        for line in response_text.strip().splitlines()
        if '. ' in line
    ]

    return suggestions
