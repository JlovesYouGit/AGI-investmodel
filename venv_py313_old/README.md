# Trade-MCP Python Virtual Environment (OLD)

This is the old virtual environment for the Trade-MCP project.

## Environment Details

- **Python Version**: 3.11.9
- **Purpose**: Previous development environment that is no longer maintained
- **Status**: Deprecated - DO NOT USE

## Why This Environment is Deprecated

This environment was originally created with a different Python version that caused compatibility issues with several dependencies. Although it now shows Python 3.11.9, it may have residual configuration issues and outdated dependencies.

Known issues with this environment:
- Potential compatibility issues with duckduckgo-search
- Possible issues with tokenizers and other packages requiring C extensions
- Outdated dependency versions

## Migration

All development has been migrated to the Python 3.11.9 environment located in `venv311`.

## Warning

Do not use this environment for development or production. It is kept only for reference and will be removed in a future release.

To verify you're NOT using this environment, ensure that:

```cmd
echo %VIRTUAL_ENV%
```

Does NOT point to this directory.