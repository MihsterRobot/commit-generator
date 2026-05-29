import pytest
from unittest.mock import patch, MagicMock

from commit_generator.diff import get_diff


def test_returns_stdin_when_piped():
    with patch("sys.stdin.isatty", return_value=False), \
         patch("sys.stdin.read", return_value="diff --git a/file.py b/file.py\n+added line"):
        result = get_diff()
        assert result == "diff --git a/file.py b/file.py\n+added line"


def test_calls_git_diff_staged_when_tty():
    mock_result = MagicMock()
    mock_result.stdout = "diff --git a/file.py b/file.py\n+added line"

    with patch("sys.stdin.isatty", return_value=True), \
         patch("subprocess.run", return_value=mock_result) as mock_run:
        result = get_diff()
        mock_run.assert_called_once_with(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True
        )
        assert result == mock_result.stdout


def test_calls_git_diff_without_staged_when_unstaged():
    mock_result = MagicMock()
    mock_result.stdout = "diff --git a/file.py b/file.py\n+added line"

    with patch("sys.stdin.isatty", return_value=True), \
         patch("subprocess.run", return_value=mock_result) as mock_run:
        result = get_diff(unstaged=True)
        mock_run.assert_called_once_with(
            ["git", "diff"],
            capture_output=True,
            text=True
        )


def test_raises_system_exit_when_diff_empty():
    mock_result = MagicMock()
    mock_result.stdout = ""

    with patch("sys.stdin.isatty", return_value=True), \
         patch("subprocess.run", return_value=mock_result):
        with pytest.raises(SystemExit) as exc_info:
            get_diff()
        assert exc_info.value.code == 1
