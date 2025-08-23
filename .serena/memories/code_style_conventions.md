# Code Style and Conventions - MD-QD Project

## Code Style Analysis

Based on the existing codebase, here are the established conventions:

### Python Style Guidelines

#### Function and Variable Naming
- **Function names**: `snake_case` (e.g., `split_into_sentences`, `chunk_markdown_file`)
- **Variable names**: `snake_case` (e.g., `current_h1`, `sentence_match`, `heading_content`)
- **Constants**: Not explicitly defined, but should follow `UPPER_CASE` convention

#### Function Structure
- **Docstrings**: Simple docstring format with brief description
  ```python
  def function_name(param):
      """Brief description of what the function does."""
      # implementation
  ```

#### Code Organization
- **Imports**: Standard library imports first, then third-party
- **File structure**: Helper functions first, main processing function, then main() at bottom
- **Main guard**: Uses `if __name__ == "__main__":` pattern

#### Error Handling
- **Encoding**: Explicit UTF-8 encoding for file operations: `encoding='utf-8'`
- **File operations**: Uses context managers (`with open()`)
- **Defensive programming**: Checks for empty strings and None values

#### Regex and Text Processing
- **Regex patterns**: Complex patterns broken into readable parts
- **String operations**: Extensive use of `.strip()` and `.split()`
- **Text cleaning**: Multiple validation steps to ensure clean data

### Specific Conventions Observed

#### Data Structures
- **Return values**: Consistent dictionary structure for sentence data:
  ```python
  {
      'text': sentence,
      'source_file': filename,
      'chapter_name': current_h1,
      'section_name': current_h2,
      'subsection_name': current_h3
  }
  ```

#### Comment Style
- **Inline comments**: Used to explain complex regex patterns and logic
- **Block comments**: Used to separate logical sections
- **TODO/NOTE**: Not observed in current code

#### Configuration Management (Qdrant Module)
- **YAML configuration**: Preferred over hardcoded values
- **Environment variables**: Used for sensitive data (API keys)
- **Default values**: Provided for all configuration options

### Recommended Adherence

#### Type Hints (Not Currently Used)
Consider adding type hints for better code documentation:
```python
def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences using regex pattern."""
```

#### Logging (Not Currently Used)
Consider adding logging instead of print statements:
```python
import logging
logging.info(f"Processed {md_file_path} -> {json_file_path}")
```

#### Error Handling Enhancement
Add try-catch blocks for file operations:
```python
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    logging.error(f"File not found: {file_path}")
    return None
```

### Project-Specific Patterns

#### Heading Processing
- Only track H1, H2, H3 levels (ignore H4+)
- Extract titles using intelligent content separation
- Handle inline content after headings

#### Text Chunking
- Sentence-level granularity
- Preserve hierarchical context
- Clean empty/whitespace-only entries

#### File Naming
- Input: `.md` files
- Output: `.json` files (same name, different extension)
- Maintain directory structure

### Dependencies Philosophy
- **Minimal dependencies**: Main chunking uses only standard library
- **Specialized tools**: Qdrant upload module uses specific libraries
- **Optional dependencies**: UI uses tkinter (standard library)

This style prioritizes readability, maintainability, and robustness while keeping dependencies minimal for the core functionality.