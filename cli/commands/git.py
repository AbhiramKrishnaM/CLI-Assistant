"""Git operations assistance."""
import os
import subprocess
import typer
from typing import Optional

app = typer.Typer(help="Git operations assistance")

def _run_git_command(cmd):
    """Run a git command and return the output."""
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"

@app.command()
def generate_commit(
    message_type: str = typer.Option("conventional", help="Commit message type (conventional or descriptive)"),
    files: Optional[bool] = typer.Option(False, "--files", "-f", help="Show changed files in the message"),
):
    """Generate a commit message for the current changes."""
    # Get changed files
    status_output = _run_git_command(["git", "status", "--porcelain"])
    
    if not status_output or status_output.startswith("Error"):
        if "Error" in status_output:
            typer.echo(status_output, err=True)
        else:
            typer.echo("No changes to commit.", err=True)
        return
    
    # Process changed files
    changes = []
    for line in status_output.splitlines():
        if line:
            status = line[:2].strip()
            file_path = line[3:]
            changes.append((status, file_path))
    
    # Generate the commit message
    if message_type == "conventional":
        # Mock conventional commit message
        commit_type = "feat"
        if any(file_path.endswith((".md", ".txt")) for _, file_path in changes):
            commit_type = "docs"
        elif any(file_path == "package.json" or file_path.endswith(".lock") for _, file_path in changes):
            commit_type = "chore"
        elif any("test" in file_path for _, file_path in changes):
            commit_type = "test"
        
        msg = f"{commit_type}: update "
        if len(changes) == 1:
            _, file_path = changes[0]
            msg += os.path.basename(file_path)
        else:
            most_common_dir = os.path.dirname(changes[0][1]) if "/" in changes[0][1] else ""
            msg += most_common_dir if most_common_dir else "multiple files"
    else:
        # Descriptive message
        actions = []
        if any(status == "M" for status, _ in changes):
            actions.append("Update")
        if any(status == "A" for status, _ in changes):
            actions.append("Add")
        if any(status == "D" for status, _ in changes):
            actions.append("Remove")
        
        msg = " & ".join(actions)
        file_count = len(changes)
        msg += f" {file_count} " + ("file" if file_count == 1 else "files")
    
    # Add files to the message if requested
    if files and changes:
        files_list = "\n\n- " + "\n- ".join(f"{status}: {file_path}" for status, file_path in changes)
        msg += files_list
    
    typer.echo(f"Generated commit message:\n\n{msg}")
    
    # Ask to use the message
    if typer.confirm("Use this commit message?"):
        result = _run_git_command(["git", "commit", "-m", msg])
        typer.echo(result)

@app.command()
def pr_description():
    """Generate a pull request description based on commits."""
    # Get commits that would be included in a PR
    try:
        main_branch = "main"
        if not _run_git_command(["git", "show-ref", "--verify", "--quiet", f"refs/heads/{main_branch}"]):
            main_branch = "master"
        
        commits = _run_git_command(["git", "log", f"{main_branch}..HEAD", "--pretty=format:%s"])
        
        if not commits:
            typer.echo("No commits found between current branch and main/master.", err=True)
            return
        
        typer.echo("Based on your commits, here's a suggested PR description:\n")
        
        # Generate title from branch name
        branch = _run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()
        title = branch.replace("-", " ").replace("_", " ").title()
        if title.startswith("Feature "):
            title = title[8:]  # Remove "Feature " prefix
        
        # Generate PR description
        description = f"# {title}\n\n## Changes\n\n"
        
        # Group commits by type for conventional commits
        commit_groups = {}
        for line in commits.splitlines():
            if ":" in line:
                commit_type, message = line.split(":", 1)
                if commit_type not in commit_groups:
                    commit_groups[commit_type] = []
                commit_groups[commit_type].append(message.strip())
            else:
                if "Other" not in commit_groups:
                    commit_groups["Other"] = []
                commit_groups["Other"].append(line.strip())
        
        for group, messages in commit_groups.items():
            description += f"### {group.capitalize()}\n"
            for msg in messages:
                description += f"- {msg}\n"
            description += "\n"
        
        description += "## Testing\n\n- [ ] Tests added for new functionality\n- [ ] All tests passing\n\n"
        description += "## Screenshots (if applicable)\n\n_Add screenshots here_\n"
        
        typer.echo(description)
    except Exception as e:
        typer.echo(f"Error generating PR description: {str(e)}", err=True) 