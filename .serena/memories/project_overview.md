# MD-QD Project Overview

## Project Purpose
The md-qd project is a markdown processing and vector database upload system designed to:

1. **Chunk Markdown Files**: Convert markdown files into structured JSON with sentence-level chunking while preserving hierarchical context (chapters, sections, subsections)
2. **Upload to Qdrant**: Take the chunked JSON data and upload it to a Qdrant vector database with automatic embedding generation for semantic search capabilities

## Project Structure
- `chunk_markdown.py` - Main script for processing markdown files into chunked JSON format
- `qdrant_upload/` - Complete Qdrant upload system with configuration and documentation
- `tests/` - Test data including sample markdown and JSON files
- `requirements.txt` - Dependencies for the markdown chunking (currently none - uses standard library only)

## Tech Stack
- **Core Language**: Python 3.8+
- **Markdown Processing**: Uses Python standard library (regex, json, tkinter for file dialogs)
- **Vector Database**: Qdrant client library
- **Embeddings**: OpenAI text-embedding models (text-embedding-3-small by default)
- **Configuration**: YAML-based configuration files
- **Environment Management**: python-dotenv for API keys

## Data Flow
1. Markdown files → `chunk_markdown.py` → Structured JSON with hierarchical metadata
2. JSON files → `qdrant_upload/upload_to_qdrant.py` → Qdrant vector database with embeddings

## Key Features
- Intelligent heading extraction and content separation
- Hierarchical context preservation (H1, H2, H3 levels only)
- Sentence-level chunking with regex-based splitting
- Batch processing for large datasets
- Comprehensive error handling and logging
- Flexible configuration system