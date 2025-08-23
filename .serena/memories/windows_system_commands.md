# Windows System Commands - MD-QD Project

## Essential Windows Commands for Development

### File System Navigation
```cmd
# Directory operations
dir                    # List current directory contents
dir /s                # List all files recursively
dir *.py              # List Python files only
cd path\to\directory  # Change directory
cd ..                 # Go up one level
cd \                  # Go to root drive
pushd path            # Save current dir and change
popd                  # Return to saved directory

# Path information
pwd                   # Current directory (PowerShell)
echo %CD%            # Current directory (CMD)
```

### File Operations
```cmd
# File content viewing
type filename.txt     # Display file contents
more filename.txt     # Display file contents with pagination
notepad filename.txt  # Open in Notepad

# File management
copy source dest      # Copy files
move source dest      # Move/rename files
del filename         # Delete files
md dirname           # Create directory
rd dirname           # Remove directory (empty)
rd /s dirname        # Remove directory recursively
```

### Search Operations
```cmd
# Find files
where filename               # Find executable files
where /r . *.py             # Find Python files recursively
dir /s /b *.json            # Find JSON files (bare format)

# Search within files
findstr "text" *.py         # Search for text in Python files
findstr /s /i "text" *.*    # Case-insensitive recursive search
findstr /n "function" *.py  # Show line numbers
```

### Process Management
```cmd
# Task management
tasklist                    # Show running processes
tasklist | findstr python  # Find Python processes
taskkill /im python.exe    # Kill Python processes
taskkill /pid 1234         # Kill by process ID
```

### Network and System
```cmd
# Network
ping google.com            # Test connectivity
ipconfig                   # Show network configuration
netstat -an               # Show network connections

# System information
systeminfo                # System information
ver                       # Windows version
whoami                    # Current user
```

### Environment Variables
```cmd
# View environment variables
set                       # Show all variables
echo %PATH%              # Show PATH variable
echo %USERPROFILE%       # Show user directory

# Set environment variables (current session)
set OPENAI_API_KEY=your-key-here
set PYTHONPATH=%PYTHONPATH%;C:\your\path

# Set permanent environment variables (requires restart)
setx OPENAI_API_KEY "your-key-here"
```

### PowerShell Alternatives (More Modern)
```powershell
# File operations
Get-ChildItem            # List directory (ls equivalent)
Get-ChildItem -Recurse   # List recursively
Get-Content filename.txt # Display file contents
Set-Location path        # Change directory (cd equivalent)

# Search operations
Select-String "pattern" *.py        # Search in files (grep equivalent)
Get-ChildItem -Recurse -Filter *.py # Find Python files

# System operations
Get-Process              # List processes
Stop-Process -Name python # Stop Python processes
Get-Service             # List services
```

### Git Integration (if Git is installed)
```cmd
# Repository operations
git status              # Check repository status
git add .              # Stage all changes
git commit -m "message" # Commit changes
git push               # Push to remote
git pull               # Pull from remote
git log --oneline      # Show commit history

# Branch operations
git branch             # List branches
git checkout -b newbranch # Create and switch to new branch
git merge branch       # Merge branch
```

### Development Workflow Commands
```cmd
# Python virtual environment (Windows)
python -m venv .venv           # Create virtual environment
.venv\Scripts\activate         # Activate virtual environment
.venv\Scripts\deactivate       # Deactivate virtual environment

# Package management
pip list                       # Show installed packages
pip install package_name       # Install package
pip install -r requirements.txt # Install from requirements
pip freeze > requirements.txt  # Generate requirements file

# Project-specific commands
python chunk_markdown.py       # Run main chunking script
cd qdrant_upload & python upload_to_qdrant.py --help # Show upload help
```

### Batch File Creation
Create `.bat` files for common tasks:

```batch
@echo off
REM activate_env.bat
call .venv\Scripts\activate
echo Virtual environment activated
cmd /k
```

```batch
@echo off
REM run_chunk.bat
python chunk_markdown.py
pause
```

### File Associations and Shortcuts
```cmd
# Open files with default applications
start filename.txt     # Open with default app
start .               # Open current directory in Explorer
start "" "C:\Program Files\..." # Start application
```

These commands provide the essential toolkit for Windows development in the md-qd project environment.