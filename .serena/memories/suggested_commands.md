# Suggested Commands for MD-QD Project

## Main Processing Commands

### Markdown Chunking
```bash
# Process markdown files to JSON (interactive file dialog)
python chunk_markdown.py

# Alternative: Process specific file programmatically
python -c "
from chunk_markdown import chunk_markdown_file
import json
result = chunk_markdown_file('input.md', 'input.md')
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)
"
```

### Qdrant Upload Commands
```bash
# Navigate to upload directory
cd qdrant_upload

# Install Qdrant upload dependencies
pip install -r requirements.txt

# Basic upload with default settings
python upload_to_qdrant.py --json-file ../tests/CBT/Self_Administered_CBT.json --collection-name cbt_documents

# Upload with custom configuration
python upload_to_qdrant.py --config qdrant_config.yaml --json-file ../tests/CBT/Self_Administered_CBT.json

# Create default configuration file
python upload_to_qdrant.py --create-config qdrant_config.yaml

# Recreate collection (delete existing)
python upload_to_qdrant.py --json-file data.json --collection-name my_docs --recreate-collection

# Test the upload system
python test_upload.py
```

## Setup Commands

### Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

# Install main project dependencies (none currently for chunking)
pip install -r requirements.txt

# Install Qdrant upload dependencies
cd qdrant_upload
pip install -r requirements.txt
cd ..
```

### Qdrant Setup
```bash
# Run local Qdrant instance via Docker
docker run -p 6333:6333 qdrant/qdrant

# Or use docker-compose (if available)
docker-compose up -d qdrant
```

### OpenAI API Configuration
```bash
# Set environment variable (Windows)
set OPENAI_API_KEY=your-api-key-here

# Set environment variable (Linux/Mac)
export OPENAI_API_KEY=your-api-key-here

# Or create .env file in qdrant_upload directory
echo "OPENAI_API_KEY=your-api-key-here" > qdrant_upload/.env
```

## Development Commands

### File Operations (Windows)
```cmd
# List directory contents
dir
dir /s  # recursive

# Find files
where /r . *.py
where /r . *.md

# View file contents
type filename.txt
more filename.txt

# Search in files
findstr "search_term" *.py
findstr /s /i "search_term" *.*  # case-insensitive, recursive
```

### Git Commands
```bash
# Initialize repository
git init

# Add and commit files
git add .
git commit -m "Initial commit"

# Check status
git status
git log --oneline

# Create and switch branches
git checkout -b feature-branch
git switch main  # newer syntax
```

## Testing Commands

### Quick Test Workflow
```bash
# 1. Test markdown chunking
python chunk_markdown.py
# (Select tests/CBT/Self_Administered_CBT.md in dialog)

# 2. Check generated JSON
type tests\CBT\Self_Administered_CBT.json

# 3. Test Qdrant upload (requires local Qdrant running)
cd qdrant_upload
python test_upload.py
```

## Project Maintenance

### Dependency Management
```bash
# Check for outdated packages
pip list --outdated

# Update packages
pip install --upgrade package_name

# Generate requirements
pip freeze > requirements.txt
```

### Code Quality
```bash
# Format code (if using black)
pip install black
black chunk_markdown.py

# Lint code (if using flake8)
pip install flake8
flake8 chunk_markdown.py

# Type checking (if using mypy)
pip install mypy
mypy chunk_markdown.py
```