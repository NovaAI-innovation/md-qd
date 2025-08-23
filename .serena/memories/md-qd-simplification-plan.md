# MD-QD Simplification Plan

## Current State Analysis
The md-qd project has expanded significantly beyond its intended purpose as a simple Model Context Protocol (MCP) server. It currently includes:

### Core MCP Functionality (Keep):
- `md_qd/server.py` - MCP server implementation with 5 tools
- `md_qd/models.py` - Pydantic data models
- `md_qd/processor.py` - Core markdown processing logic
- `run_server.py` - Server entry point
- Basic dependencies: markdown, python-frontmatter, beautifulsoup4, pydantic

### Additional Functionality (Remove):
1. **CLI Interface**: `md_qd/cli.py`, `run_cli.py` - Complete CLI with convert/analyze/serve commands
2. **Library Examples**: `examples.py` - Demonstration of library usage patterns
3. **Demo Scripts**: `quickstart.py`, `test_md_qd.py` - Quick start and test generation
4. **Setup Infrastructure**: Multiple setup scripts (.py, .bat, .sh files)
5. **Development Tools**: Extensive documentation, multiple entry points
6. **Utility Functions**: Some functions in `md_qd/utils.py` may be excessive for MCP-only usage

## Simplification Goals:
1. Remove all CLI functionality
2. Remove demo and example scripts
3. Remove complex setup infrastructure
4. Simplify dependencies and project structure
5. Keep only essential MCP server functionality
6. Maintain core markdown processing capabilities
7. Preserve the 5 MCP tools: convert_directory, convert_file, configure_chunking, get_conversion_stats, get_current_config

## Essential Files to Keep:
- `md_qd/server.py` 
- `md_qd/models.py`
- `md_qd/processor.py` 
- `md_qd/mcp_fallback.py` (for MCP compatibility)
- `run_server.py`
- `pyproject.toml` (simplified)
- `README.md` (simplified)
- Essential parts of `md_qd/utils.py`

## Files to Remove:
- `md_qd/cli.py`
- `run_cli.py` 
- `examples.py`
- `quickstart.py`
- `test_md_qd.py`
- Setup scripts (install.py, setup_*.py, setup_dev.*)
- Documentation files (API.md, USAGE.md, CONTRIBUTING.md, CHANGELOG.md)
