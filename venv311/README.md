# Trade-MCP Python Virtual Environment

This is the official virtual environment for the Trade-MCP project.

## Environment Details

- **Python Version**: 3.11.9
- **Purpose**: Main development and production environment
- **Status**: Active

## Setup Instructions

To activate this environment:

```cmd
venv311\Scripts\activate.bat
```

or

```powershell
venv311\Scripts\Activate.ps1
```

## Dependencies

All project dependencies are installed in this environment. To install or update dependencies:

```cmd
pip install -r requirements.txt
```

## Verification

To verify you're using the correct environment:

```cmd
python --version
```

Should output: `Python 3.11.9`

And:

```cmd
echo %VIRTUAL_ENV%
```

Should output the path to this directory.