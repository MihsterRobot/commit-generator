commit-generator
Generate conventional commit message suggestions from a git diff using the Anthropic API.
Demo
# Automatic (reads staged diff)

python -m commit_generator

# Suggested commit messages:

#   1. feat(auth): add JWT expiry validation to login handler

#   2. fix(auth): correct token expiry check in session middleware

#   3. refactor(login): extract token validation into helper function
Features
Reads staged diff automatically or accepts piped input via stdin
Generates 2–3 conventional commit message suggestions by default
--apply flag for interactively selecting and applying a suggestion as a commit
Truncates large diffs automatically to stay within context limits
Installation
git clone https://github.com/MihsterRobot/commit-generator.git

cd commit-generator

python -m venv venv

venv\Scripts\activate  # Windows

pip install -e .

Create a .env file in the project root:

ANTHROPIC_API_KEY=your_key_here
Usage
# Generate suggestions from staged diff

python -m commit_generator

# Pipe a diff manually

git diff --staged | python -m commit_generator

# Use unstaged changes

python -m commit_generator --unstaged

# Select a suggestion and apply it as a commit

python -m commit_generator --apply

# Control number of suggestions (default: 3)

python -m commit_generator --count 2
Project Structure
commit_generator/

├── cli.py        # Argument parsing and entry point

├── diff.py       # Diff acquisition via subprocess or stdin

├── llm.py        # Anthropic API call and suggestion parsing

└── git.py        # Interactive commit application

tests/

├── test_diff.py

├── test_llm.py

└── test_git.py

Running Tests
pip install pytest

pytest
