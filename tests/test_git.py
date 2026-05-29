from unittest.mock import patch, MagicMock

import pytest

from commit_generator.git import apply_suggestion

SUGGESTIONS = [
    'feat(auth): add JWT validation',
    'feat(login): validate token expiry',
    'fix(auth): correct token expiry check'
]


def test_commits_with_selected_suggestion():
    mock_result = MagicMock()
    mock_result.returncode = 0

    with patch('builtins.input', side_effect=['1', 'y']), \
         patch('subprocess.run', return_value=mock_result) as mock_run:
        apply_suggestion(SUGGESTIONS)
        mock_run.assert_called_once_with(
            ['git', 'commit', '-m', SUGGESTIONS[0]]
        )


def test_raises_system_exit_on_non_digit_input():
    with patch('builtins.input', return_value='x'):
        with pytest.raises(SystemExit) as exc_info:
            apply_suggestion(SUGGESTIONS)
        assert exc_info.value.code == 1


def test_raises_system_exit_on_out_of_range_input():
    with patch('builtins.input', return_value='99'):
        with pytest.raises(SystemExit) as exc_info:
            apply_suggestion(SUGGESTIONS)
        assert exc_info.value.code == 1


def test_raises_system_exit_on_declined_confirmation():
    with patch('builtins.input', side_effect=['1', 'n']):
        with pytest.raises(SystemExit) as exc_info:
            apply_suggestion(SUGGESTIONS)
        assert exc_info.value.code == 0


def test_propagates_git_return_code_on_failure():
    mock_result = MagicMock()
    mock_result.returncode = 1

    with patch('builtins.input', side_effect=['1', 'y']), \
         patch('subprocess.run', return_value=mock_result):
        with pytest.raises(SystemExit) as exc_info:
            apply_suggestion(SUGGESTIONS)
        assert exc_info.value.code == 1
