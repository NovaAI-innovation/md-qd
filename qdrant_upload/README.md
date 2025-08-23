# Qdrant Upload Script

A Python script for uploading chunked JSON files to Qdrant vector database with automatic embedding generation.

## Features

- **Automatic Embedding Generation**: Uses OpenAI's text-embedding-3-small model to generate vector embeddings
- **Batch Processing**: Efficiently uploads large datasets in configurable batches
- **Metadata Preservation**: Maintains all JSON metadata fields in Qdrant payloads
- **Flexible Configuration**: Supports both command-line arguments and YAML configuration files
- **Error Handling**: Robust error handling with detailed logging
- **Collection Management**: Can create, recreate, and manage Qdrant collections

## Prerequisites

- Python 3.8 or higher
- Qdrant instance running (local or cloud)
- Internet connection (for OpenAI API calls)
- OpenAI API key (set via OPENAI_API_KEY environment variable)

## Installation

1. **Clone or download the script files** to your local directory

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python upload_to_qdrant.py --help
   ```

## Quick Start

### 1. Set up OpenAI API Key

**Option A: Using .env file (recommended)**
Create a `.env` file in the project directory:
```bash
# Copy the example file and edit it
cp openai_config.env .env
# Then edit .env with your actual API key
```

**Option B: Export environment variable**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 2. Qdrant Setup

**Qdrant Cloud (default configuration)**:
The uploader is pre-configured to use Qdrant Cloud. Your `qdrant_config.yaml` already contains the cloud connection details.

**For local testing (optional)**:
If you want to test locally, update your config:
```bash
# Edit qdrant_config.yaml
qdrant_host: localhost
qdrant_port: 6333
qdrant_api_key: null

# Then start local Qdrant:
docker run -p 6333:6333 qdrant/qdrant
```

### 3. Upload Your JSON File

**Basic usage**:
```bash
python upload_to_qdrant.py --json-file ../tests/CBT/Self_Administered_CBT.json --collection-name cbt_documents
```

**With configuration file**:
```bash
python upload_to_qdrant.py --config qdrant_config.yaml --json-file ../tests/CBT/Self_Administered_CBT.json
```

## Configuration

### Create Default Configuration

Generate a default configuration file:
```bash
python upload_to_qdrant.py --create-config qdrant_config.yaml
```

### Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `qdrant_host` | Qdrant server hostname or cloud URL | `https://75f5cc60-af58-46dd-8e92-16ff874b8b8c.us-east4-0.gcp.cloud.qdrant.io` |
| `qdrant_port` | Qdrant server port (ignored for cloud) | `6333` |
| `qdrant_api_key` | API key for authentication | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.RQmW_5jzMpwqbws5PnYFwW7hh0FFW6AejFLKNNHYfAs` |
| `collection_name` | Name of the collection | `cbt_documents` |
| `embedding_model` | OpenAI embedding model | `text-embedding-3-small` |
| `batch_size` | Documents per batch | `100` |
| `recreate_collection` | Delete existing collection | `false` |

### Cloud vs Local Configuration

**Cloud Configuration (Default)**:
- Uses your pre-configured Qdrant Cloud instance
- Automatically detects HTTPS URLs and uses cloud connection
- Requires valid API key in configuration

**Local Configuration**:
- Set `qdrant_host` to `localhost` or your local IP
- Set `qdrant_port` to your local Qdrant port (usually 6333)
- Set `qdrant_api_key` to `null` for unsecured local instances

### Embedding Models

The script supports various OpenAI embedding models:

- **`text-embedding-3-small`** (1536d) - Fast, good quality, recommended for most use cases
- **`text-embedding-3-large`** (3072d) - Higher quality, slower processing
- **`text-embedding-ada-002`** (1536d) - Legacy model, still effective

## Usage Examples

### Command Line Usage

**Upload with custom collection name**:
```bash
python upload_to_qdrant.py \
  --json-file data.json \
  --collection-name my_documents \
  --batch-size 50
```

**Recreate existing collection**:
```bash
python upload_to_qdrant.py \
  --json-file data.json \
  --collection-name my_documents \
  --recreate-collection
```

**Use custom configuration**:
```bash
python upload_to_qdrant.py \
  --config my_config.yaml \
  --json-file data.json
```

### Configuration File Usage

1. **Copy and modify the sample config**:
   ```bash
   cp qdrant_config.yaml my_config.yaml
   # Edit my_config.yaml with your settings
   ```

2. **Use the configuration**:
   ```bash
   python upload_to_qdrant.py --config my_config.yaml --json-file data.json
   ```

## JSON Data Format

The script expects JSON files with the following structure:

```json
[
  {
    "text": "The main text content to be embedded",
    "source_file": "document.md",
    "chapter_name": "Chapter 1",
    "section_name": "Introduction",
    "subsection_name": "Overview"
  },
  {
    "text": "Another text chunk...",
    "source_file": "document.md",
    "chapter_name": "Chapter 1",
    "section_name": "Introduction",
    "subsection_name": null
  }
]
```

**Required fields**:
- `text`: The text content to be vectorized

**Optional metadata fields** (will be stored in Qdrant payload):
- `source_file`: Source document filename
- `chapter_name`: Chapter or section name
- `section_name`: Subsection name
- `subsection_name`: Sub-subsection name
- Any other custom fields you add

## Advanced Usage

### Custom Embedding Models

To use a different OpenAI embedding model, update your config:

```yaml
embedding_model: text-embedding-3-large  # Higher quality, 3072 dimensions
# Available models:
# - text-embedding-3-small (1536d, efficient)
# - text-embedding-3-large (3072d, higher quality)
# - text-embedding-ada-002 (1536d, legacy)
```

### Cloud Qdrant Setup

For Qdrant Cloud or secured instances:

```yaml
qdrant_host: your-instance.qdrant.io
qdrant_port: 6333
qdrant_api_key: your-api-key-here
```

### Large Dataset Processing

For very large datasets, adjust batch size:

```yaml
batch_size: 50  # Smaller batches for memory-constrained environments
```

## Troubleshooting

### Common Issues

**Connection refused**:
- Ensure Qdrant is running
- Check host/port configuration
- Verify firewall settings

**Out of memory**:
- Reduce batch size
- Use text-embedding-3-small instead of text-embedding-3-large
- Process files in smaller chunks

**OpenAI API issues**:
- Check OPENAI_API_KEY environment variable is set
- Verify API key has sufficient credits
- Check internet connection
- Try different embedding model

### Debug Mode

Enable verbose logging by modifying the script:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Performance Tips

1. **Batch Size**: Optimal batch size depends on your hardware. Start with 100 and adjust.
2. **Embedding Model**: `all-MiniLM-L6-v2` offers good balance of speed and quality.
3. **Collection Management**: Use `recreate_collection: false` for incremental updates.
4. **Network**: For cloud deployments, ensure stable network connection.

## Monitoring

The script provides detailed progress information:
- Document loading progress
- Embedding generation progress
- Batch upload progress
- Final collection statistics

## Security Considerations

- **API Keys**: Store API keys securely, never commit them to version control
- **Network Access**: Restrict Qdrant access to trusted networks
- **Data Privacy**: Ensure your data handling complies with privacy regulations

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Qdrant documentation: https://qdrant.tech/documentation/
3. Check OpenAI embeddings documentation: https://platform.openai.com/docs/guides/embeddings

## License

This script is provided as-is for educational and development purposes.

