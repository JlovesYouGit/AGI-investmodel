#!/usr/bin/env python3
"""
CODE_HAWK: A stateful code-quality daemon that never sleeps.
Performs comprehensive code quality scanning and fixing.
"""

import os
import subprocess
import re
from typing import List, Tuple

# Global lists
TODO_FILE = "TODO_FILE.md"
DONE_FILE = "DONE_FILE.md"

def initialize_files():
    """Initialize TODO and DONE files."""
    if not os.path.exists(TODO_FILE):
        with open(TODO_FILE, "w") as f:
            f.write("# TODO_FILE\n\n")
    if not os.path.exists(DONE_FILE):
        with open(DONE_FILE, "w") as f:
            f.write("# DONE_FILE\n\n")

def run_command(cmd: str, cwd: str = None) -> Tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, and stderr."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def scan_python_files() -> List[str]:
    """Scan Python files with various linters."""
    issues = []
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk("."):
        # Skip virtual environments and node_modules
        dirs[:] = [d for d in dirs if not d.startswith("venv") and d != "node_modules" and d != ".git"]
        for file in files:
            if file.endswith(".py") and not file.startswith("test_"):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files to scan")
    
    # Run ruff
    for py_file in python_files:
        # Ruff check
        exit_code, stdout, stderr = run_command(f"python -m ruff check {py_file}")
        if exit_code != 0:
            # Parse ruff output
            lines = (stdout + stderr).split('\n')
            for line in lines:
                if ':' in line and py_file in line:
                    issues.append(f"{line.strip()}")
        
        # Pylint check
        exit_code, stdout, stderr = run_command(f"pylint {py_file} --output-format=text")
        if exit_code != 0 and "has been rated" not in stdout:
            # Parse pylint output
            lines = (stdout + stderr).split('\n')
            for line in lines:
                if ':' in line and py_file in line:
                    issues.append(f"{line.strip()}")
        
        # Bandit security check
        exit_code, stdout, stderr = run_command(f"bandit -r {py_file} -f txt")
        if exit_code == 1:  # Bandit returns 1 for issues found
            lines = (stdout + stderr).split('\n')
            for line in lines:
                if '>>' in line or 'Issue:' in line:
                    issues.append(f"BANDIT:{py_file}:1:1:bandit:HIGH:security:{line.strip()}")
    
    return issues

def scan_typescript_files() -> List[str]:
    """Scan TypeScript files with ESLint."""
    issues = []
    
    # Find all TypeScript files
    ts_files = []
    for root, dirs, files in os.walk("."):
        # Skip virtual environments and node_modules
        dirs[:] = [d for d in dirs if not d.startswith("venv") and d != "node_modules" and d != ".git"]
        for file in files:
            if file.endswith(".ts") or file.endswith(".tsx"):
                ts_files.append(os.path.join(root, file))
    
    print(f"Found {len(ts_files)} TypeScript files to scan")
    
    # Run ESLint on TypeScript files
    if ts_files:
        files_str = " ".join(ts_files)
        exit_code, stdout, stderr = run_command(f"eslint {files_str} --ext .ts,.tsx")
        if exit_code != 0:
            # Parse ESLint output
            lines = (stdout + stderr).split('\n')
            for line in lines:
                if ':' in line and ('error' in line.lower() or 'warning' in line.lower()):
                    issues.append(f"{line.strip()}")
    
    return issues

def scan_todo_fixme() -> List[str]:
    """Scan for TODO/FIXME comments."""
    issues = []
    
    # Find all code files
    code_files = []
    for root, dirs, files in os.walk("."):
        # Skip virtual environments and node_modules
        dirs[:] = [d for d in dirs if not d.startswith("venv") and d != "node_modules" and d != ".git"]
        for file in files:
            if file.endswith((".py", ".ts", ".tsx", ".js", ".jsx")):
                code_files.append(os.path.join(root, file))
    
    # Scan for TODO/FIXME
    for file_path in code_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines, 1):
                    if 'TODO' in line or 'FIXME' in line:
                        # Check if it's older than 7 days (simplified check)
                        issues.append(f"{file_path}:{i}:1:custom:WARNING:todo_fixme:Found TODO/FIXME comment")
        except Exception:
            # Skip files that can't be read
            pass
    
    return issues

def write_todo_file(issues: List[str]):
    """Write issues to TODO_FILE."""
    with open(TODO_FILE, "w") as f:
        f.write("# TODO_FILE\n\n")
        for issue in issues:
            # Convert to standard format if not already
            if not re.match(r'^[^:]+:\d+:\d+:[^:]+:[^:]+:[^:]+:.+', issue):
                # Try to parse different formats
                if 'error' in issue.lower() or 'warning' in issue.lower():
                    f.write(f"- [ ] CUSTOM:1:1:custom:WARNING:parse_error:{issue}\n")
                else:
                    f.write(f"- [ ] {issue}\n")
            else:
                f.write(f"- [ ] {issue}\n")

def main():
    """Main scanning function."""
    print("CODE_HAWK: Starting boot-up scan...")
    initialize_files()
    
    all_issues = []
    
    # Scan Python files
    print("Scanning Python files...")
    python_issues = scan_python_files()
    all_issues.extend(python_issues)
    
    # Scan TypeScript files
    print("Scanning TypeScript files...")
    ts_issues = scan_typescript_files()
    all_issues.extend(ts_issues)
    
    # Scan for TODO/FIXME
    print("Scanning for TODO/FIXME comments...")
    todo_issues = scan_todo_fixme()
    all_issues.extend(todo_issues)
    
    # Write to TODO file
    write_todo_file(all_issues)
    
    print(f"Scan complete. Found {len(all_issues)} issues.")
    print(f"Results written to {TODO_FILE}")

if __name__ == "__main__":
    main()