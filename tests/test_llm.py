import pytest
from unittest.mock import MagicMock, patch
from anthropic.types import TextBlock

from commit_generator.llm import get_suggestions, MAX_DIFF_CHARS


def make_mock_response(text: str) -> MagicMock:
    mock_block = MagicMock()
    mock_block.type = 'text'
    mock_block.text = text

    mock_response = MagicMock()
    mock_response.content = [TextBlock(type='text', text=text)]
    return mock_response


MOCK_RESPONSE_TEXT = '1. feat(auth): add JWT validation\n2. feat(login): validate token expiry\n3. fix(auth): correct token expiry check'


def test_returns_parsed_suggestions():
    mock_response = make_mock_response(MOCK_RESPONSE_TEXT)

    with patch('commit_generator.llm.anthropic.Anthropic') as mock_client:
        mock_client.return_value.messages.create.return_value = mock_response
        result = get_suggestions('some diff')

    assert result == [
        'feat(auth): add JWT validation',
        'feat(login): validate token expiry',
        'fix(auth): correct token expiry check'
    ]


def test_truncates_long_diff():
    long_diff = 'x' * (MAX_DIFF_CHARS + 1000)

    mock_response = make_mock_response(MOCK_RESPONSE_TEXT)

    with patch('commit_generator.llm.anthropic.Anthropic') as mock_client:
        mock_client.return_value.messages.create.return_value = mock_response
        get_suggestions(long_diff)

        call_kwargs = mock_client.return_value.messages.create.call_args
        user_message = call_kwargs.kwargs['messages'][0]['content']

    PREFIX = 'Git diff:\n\n'
    assert len(user_message) <= len(PREFIX) + MAX_DIFF_CHARS + len('\n... [diff truncated]')


def test_returns_correct_number_of_suggestions():
    mock_response = make_mock_response(MOCK_RESPONSE_TEXT)

    with patch('commit_generator.llm.anthropic.Anthropic') as mock_client:
        mock_client.return_value.messages.create.return_value = mock_response
        result = get_suggestions('some diff', count=3)

    assert len(result) == 3
