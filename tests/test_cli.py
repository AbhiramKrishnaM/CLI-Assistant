"""Tests for CLI functionality."""
import pytest
from typer.testing import CliRunner
from cli.main import app
from cli.commands import code, terminal, git, docs, api
from unittest.mock import patch

runner = CliRunner()

def test_main_help():
    """Test the main CLI help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "AI-powered CLI assistant" in result.stdout
    assert "code" in result.stdout
    assert "terminal" in result.stdout
    assert "git" in result.stdout
    assert "docs" in result.stdout
    assert "api" in result.stdout

def test_hello_command():
    """Test the hello command."""
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "Hello! AI CLI Assistant is ready to help you." in result.stdout
    assert "Available commands:" in result.stdout

def test_code_generate_command():
    """Test the code generate command."""
    result = runner.invoke(
        code.app, 
        ["generate", "A function to calculate the factorial of a number", "--language", "python"]
    )
    assert result.exit_code == 0
    assert "Generating python code for:" in result.stdout

def test_code_explain_command():
    """Test the code explain command using a mock file."""
    # This test might need a temporary file setup
    # For now, we'll just check the command help
    result = runner.invoke(code.app, ["explain", "--help"])
    assert result.exit_code == 0
    assert "Explain the provided code" in result.stdout

def test_terminal_suggest_command():
    """Test the terminal suggest command."""
    result = runner.invoke(terminal.app, ["suggest", "list all files in a directory"])
    assert result.exit_code == 0
    assert "Suggesting commands for 'list all files in a directory'" in result.stdout
    # Check that it suggests typical file listing commands
    assert "ls" in result.stdout or "dir" in result.stdout

def test_terminal_explain_command():
    """Test the terminal explain command."""
    result = runner.invoke(terminal.app, ["explain", "ls", "-la"])
    assert result.exit_code == 0
    assert "Explaining command:" in result.stdout
    assert "ls -la" in result.stdout

def test_docs_search_command():
    """Test the docs search command."""
    result = runner.invoke(docs.app, ["search", "function"])
    assert result.exit_code == 0
    assert "Searching docs for: function" in result.stdout

@patch('cli.commands.git._run_git_command')
def test_git_generate_commit(mock_run_git):
    """Test the git generate commit command."""
    # Mock git status to show modified files
    mock_run_git.return_value = "M  file1.py\nA  file2.py\n"
    
    # Run the command
    result = runner.invoke(git.app, ["generate-commit"], input="n\n")  # Answer 'no' to using the commit
    
    assert result.exit_code == 0
    assert "Generated commit message:" in result.stdout
    assert "file1.py" in result.stdout or "file2.py" in result.stdout

@patch('cli.commands.git._run_git_command')
def test_git_pr_description(mock_run_git):
    """Test the git PR description command."""
    # Mock git responses
    mock_responses = {
        ("git", "show-ref", "--verify", "--quiet", "refs/heads/main"): "",
        ("git", "log", "main..HEAD", "--pretty=format:%s"): "feat: add new feature\nfix: fix bug",
        ("git", "rev-parse", "--abbrev-ref", "HEAD"): "feature-branch",
    }
    
    def side_effect(args):
        for cmd, response in mock_responses.items():
            if all(a in args for a in cmd):
                return response
        return ""
    
    mock_run_git.side_effect = side_effect
    
    # Run the command
    result = runner.invoke(git.app, ["pr-description"])
    
    assert result.exit_code == 0
    assert "Based on your commits" in result.stdout
    assert "Feature Branch" in result.stdout
    assert "feat:" in result.stdout
    assert "fix:" in result.stdout 