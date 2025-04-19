#!/usr/bin/env python
"""Script to automatically fix common linting issues.

This script helps fix the most common and easily-automatable linting issues
found by flake8 in the codebase.
"""

import os
import re
from typing import Dict, List


def fix_whitespace_after_colon(filepath: str) -> int:
    """Fix missing whitespace after colon (E231).

    Args:
        filepath: Path to the file to fix

    Returns:
        Number of fixes made
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix missing whitespace after colon - not inside strings
    # This is a simple fix and may not catch all cases correctly
    pattern = r'([^\s"\']): ([^\s"\'])'
    replacement = r"\1: \2"
    new_content, count = re.subn(pattern, replacement, content)

    if count > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return count


def fix_unused_imports(filepath: str) -> int:
    """Remove unused imports (F401).

    Args:
        filepath: Path to the file to fix

    Returns:
        Number of fixes made
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Get all F401 errors from flake8
    import subprocess

    result = subprocess.run(
        ["flake8", "--select=F401", filepath], capture_output=True, text=True
    )

    if not result.stdout:
        return 0

    # Parse the line numbers and import names
    unused_imports: Dict[int, List[str]] = {}
    for line in result.stdout.splitlines():
        match = re.search(r"(\d+): (\d+): F401 \'([^\']+)\' imported but unused", line)
        if match:
            line_num = int(match.group(1)) - 1  # 0-indexed
            import_name = match.group(3)

            if line_num not in unused_imports:
                unused_imports[line_num] = []
            unused_imports[line_num].append(import_name)

    # Remove the unused imports
    fixes = 0
    new_lines = []
    for i, line in enumerate(lines):
        if i in unused_imports:
            # Handle simple cases where one import is on a line
            if line.strip().startswith("import "):
                # Skip this line entirely
                fixes += 1
                continue

            # Handle 'from x import y' cases
            if "from " in line and " import " in line:
                # Get everything after 'import '
                import_part = line.split(" import ")[1].strip()
                imports = [imp.strip() for imp in import_part.split(",")]

                # Filter out unused imports
                imports_to_keep = [
                    imp
                    for imp in imports
                    if not any(unused.endswith(imp) for unused in unused_imports[i])
                ]

                if not imports_to_keep:
                    # All imports on this line are unused
                    fixes += 1
                    continue

                # Recreate the line with only the used imports
                new_import_part = ", ".join(imports_to_keep)
                new_line = (
                    line.split(" import ")[0] + " import " + new_import_part + "\n"
                )
                new_lines.append(new_line)
                fixes += len(imports) - len(imports_to_keep)
                continue

        new_lines.append(line)

    if fixes > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    return fixes


def fix_f_strings_missing_placeholders(filepath: str) -> int:
    """Fix f-strings missing placeholders (F541).

    Args:
        filepath: Path to the file to fix

    Returns:
        Number of fixes made
    """
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Get all F541 errors from flake8
    import subprocess

    result = subprocess.run(
        ["flake8", "--select=F541", filepath], capture_output=True, text=True
    )

    if not result.stdout:
        return 0

    # Parse the line numbers
    f_string_lines = set()
    for line in result.stdout.splitlines():
        match = re.search(r"(\d+): (\d+): F541", line)
        if match:
            line_num = int(match.group(1)) - 1  # 0-indexed
            f_string_lines.add(line_num)

    # Fix the f-strings
    fixes = 0
    for i in f_string_lines:
        if i < len(lines):
            # Convert f-string to regular string
            line = lines[i]
            lines[i] = re.sub(r'f(["\'])', r"\1", line)
            fixes += 1

    if fixes > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)

    return fixes


def find_python_files(directory: str) -> List[str]:
    """Find all Python files in a directory recursively.

    Args:
        directory: Directory to search

    Returns:
        List of Python file paths
    """
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def main() -> None:
    """Main function to fix common linting errors."""
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Find all Python files
    python_files = []
    directories_to_check = ["cli", "tests", "scripts", "shared"]
    for directory in directories_to_check:
        dir_path = os.path.join(project_root, directory)
        if os.path.exists(dir_path):
            python_files.extend(find_python_files(dir_path))

    total_fixes = 0

    # Fix whitespace after colon
    print("Fixing missing whitespace after colon (E231)...")
    whitespace_fixes = 0
    for file in python_files:
        whitespace_fixes += fix_whitespace_after_colon(file)
    total_fixes += whitespace_fixes
    print(f"  Fixed {whitespace_fixes} instances of missing whitespace")

    # Fix unused imports
    print("Fixing unused imports (F401)...")
    import_fixes = 0
    for file in python_files:
        import_fixes += fix_unused_imports(file)
    total_fixes += import_fixes
    print(f"  Fixed {import_fixes} unused imports")

    # Fix f-strings missing placeholders
    print("Fixing f-strings missing placeholders (F541)...")
    f_string_fixes = 0
    for file in python_files:
        f_string_fixes += fix_f_strings_missing_placeholders(file)
    total_fixes += f_string_fixes
    print(f"  Fixed {f_string_fixes} f-strings")

    print(f"\nTotal fixes: {total_fixes}")
    print("\nFor remaining lint errors:")
    print("1. For long lines (E501): manually break up long lines")
    print(
        "2. For bare except clauses (E722): specify exceptions like 'except Exception:'"
    )
    print("3. For undefined variables (F821): define or correct the variable names")
    print("4. For unused variables (F841): remove or use the variables")
    print("\nRun 'pre-commit run --all-files' to check if all issues are fixed.")


if __name__ == "__main__":
    main()
