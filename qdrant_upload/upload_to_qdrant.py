#!/usr/bin/env python3
"""
Qdrant Upload Script for Chunked JSON Files

This script uploads chunked JSON files to a Qdrant vector database collection.
Each JSON entry should contain text content and metadata fields.

Usage:
    python upload_to_qdrant.py --json-file path/to/file.json --collection-name my_collection
    python upload_to_qdrant.py --config config.yaml
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()  # This will load .env from the current directory
except ImportError:
    # python-dotenv is optional, continue without it
    pass

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    from qdrant_client.http.models import Distance, VectorParams
    from openai import OpenAI
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install required packages:")
    print("pip install qdrant-client openai pyyaml")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QdrantUploader:
    """Handles uploading of chunked JSON files to Qdrant vector database."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the uploader with configuration."""
        self.config = config
        self.client = None
        self.openai_client = None
        self.embedding_model_name = None
        self.collection_name = config.get('collection_name', 'default_collection')
        
        # Initialize Qdrant client
        self._init_qdrant_client()
        
        # Initialize OpenAI client and embedding model
        self._init_openai_client()
    
    def _init_qdrant_client(self):
        """Initialize Qdrant client connection."""
        try:
            host = self.config.get('qdrant_host', 'localhost')
            port = self.config.get('qdrant_port', 6333)
            api_key = self.config.get('qdrant_api_key')
            
            # Check if this is a cloud connection (URL contains https://)
            if host.startswith('https://'):
                # Cloud connection - use URL directly
                self.client = QdrantClient(url=host, api_key=api_key)
                logger.info(f"Connected to Qdrant Cloud at {host}")
            else:
                # Local connection - use host and port
                if api_key:
                    self.client = QdrantClient(host=host, port=port, api_key=api_key)
                else:
                    self.client = QdrantClient(host=host, port=port)
                logger.info(f"Connected to Qdrant at {host}:{port}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise
    
    def _init_openai_client(self):
        """Initialize the OpenAI client for embeddings."""
        try:
            # Initialize OpenAI client - API key should be set via OPENAI_API_KEY environment variable
            self.openai_client = OpenAI()
            
            # Set embedding model name
            self.embedding_model_name = self.config.get('embedding_model', 'text-embedding-3-small')
            logger.info(f"Initialized OpenAI client with embedding model: {self.embedding_model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            logger.error("Make sure OPENAI_API_KEY environment variable is set")
            raise
    
    def create_collection(self, vector_size: int = 1536, recreate: bool = False):
        """Create or recreate the collection in Qdrant."""
        try:
            if recreate:
                # Delete existing collection if it exists
                try:
                    self.client.delete_collection(self.collection_name)
                    logger.info(f"Deleted existing collection: {self.collection_name}")
                except Exception:
                    pass  # Collection might not exist
            
            # Create new collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
            logger.info(f"Created collection: {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise
    
    def load_json_data(self, json_file_path: str) -> List[Dict[str, Any]]:
        """Load and validate JSON data from file."""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise ValueError("JSON data must be a list of objects")
            
            # Validate each entry has required fields
            required_fields = ['text']
            for i, entry in enumerate(data):
                if not isinstance(entry, dict):
                    raise ValueError(f"Entry {i} must be a dictionary")
                
                if 'text' not in entry:
                    raise ValueError(f"Entry {i} missing required field 'text'")
                
                if not entry['text'].strip():
                    logger.warning(f"Entry {i} has empty text, skipping")
                    continue
            
            logger.info(f"Loaded {len(data)} entries from {json_file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load JSON data: {e}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using OpenAI."""
        try:
            # Filter out empty texts
            valid_texts = [text.strip() for text in texts if text.strip()]
            
            if not valid_texts:
                return []
            
            logger.info(f"Generating embeddings for {len(valid_texts)} texts using OpenAI {self.embedding_model_name}")
            
            # Generate embeddings using OpenAI API
            response = self.openai_client.embeddings.create(
                input=valid_texts,
                model=self.embedding_model_name
            )
            
            # Extract embedding vectors from response
            embeddings = [embedding.embedding for embedding in response.data]
            
            logger.info(f"Generated embeddings for {len(embeddings)} texts")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise
    
    def upload_to_qdrant(self, data: List[Dict[str, Any]], batch_size: int = 100):
        """Upload data to Qdrant in batches."""
        try:
            total_entries = len(data)
            uploaded_count = 0
            
            # Process in batches
            for i in range(0, total_entries, batch_size):
                batch = data[i:i + batch_size]
                batch_texts = [entry['text'] for entry in batch]
                
                # Generate embeddings for this batch
                batch_embeddings = self.generate_embeddings(batch_texts)
                
                if not batch_embeddings:
                    logger.warning(f"Batch {i//batch_size + 1}: No valid embeddings generated")
                    continue
                
                # Prepare points for upload
                points = []
                for j, (entry, embedding) in enumerate(zip(batch, batch_embeddings)):
                    point_id = i + j
                    
                    # Prepare payload (metadata)
                    payload = {
                        'text': entry['text'],
                        'source_file': entry.get('source_file', ''),
                        'chapter_name': entry.get('chapter_name', ''),
                        'section_name': entry.get('section_name', ''),
                        'subsection_name': entry.get('subsection_name', '')
                    }
                    
                    # Remove None values
                    payload = {k: v for k, v in payload.items() if v is not None}
                    
                    points.append(models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=payload
                    ))
                
                # Upload batch to Qdrant
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                
                uploaded_count += len(points)
                logger.info(f"Uploaded batch {i//batch_size + 1}: {len(points)} points")
            
            logger.info(f"Successfully uploaded {uploaded_count} points to collection '{self.collection_name}'")
            return uploaded_count
            
        except Exception as e:
            logger.error(f"Failed to upload to Qdrant: {e}")
            raise
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                'name': info.name,
                'vectors_count': info.vectors_count,
                'points_count': info.points_count,
                'status': info.status
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {}


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info(f"Loaded configuration from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise


def create_default_config(config_path: str):
    """Create a default configuration file."""
    default_config = {
        'qdrant_host': 'localhost',
        'qdrant_port': 6333,
        'qdrant_api_key': None,
        'collection_name': 'cbt_documents',
        'embedding_model': 'text-embedding-3-small',
        'batch_size': 100,
        'recreate_collection': False
    }
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False, indent=2)
        logger.info(f"Created default configuration file: {config_path}")
    except Exception as e:
        logger.error(f"Failed to create config file: {e}")
        raise


def main():
    """Main function to handle command line arguments and execute upload."""
    parser = argparse.ArgumentParser(
        description='Upload chunked JSON files to Qdrant vector database'
    )
    
    parser.add_argument(
        '--json-file', '-j',
        type=str,
        help='Path to the JSON file to upload'
    )
    
    parser.add_argument(
        '--collection-name', '-c',
        type=str,
        help='Name of the Qdrant collection'
    )
    
    parser.add_argument(
        '--config', '-f',
        type=str,
        help='Path to configuration YAML file'
    )
    
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Create a default configuration file'
    )
    
    parser.add_argument(
        '--recreate-collection',
        action='store_true',
        help='Recreate the collection (delete existing)'
    )
    
    parser.add_argument(
        '--batch-size', '-b',
        type=int,
        default=100,
        help='Batch size for uploads (default: 100)'
    )
    
    args = parser.parse_args()
    
    # Handle config creation
    if args.create_config:
        config_path = args.config or 'qdrant_config.yaml'
        create_default_config(config_path)
        return
    
    # Load configuration
    if args.config:
        config = load_config(args.config)
    else:
        # Use command line arguments or defaults
        config = {
            'qdrant_host': 'localhost',
            'qdrant_port': 6333,
            'qdrant_api_key': None,
            'collection_name': args.collection_name or 'cbt_documents',
            'embedding_model': 'text-embedding-3-small',
            'batch_size': args.batch_size,
            'recreate_collection': args.recreate_collection
        }
    
    # Validate required arguments
    if not args.json_file:
        logger.error("JSON file path is required")
        parser.print_help()
        return
    
    if not os.path.exists(args.json_file):
        logger.error(f"JSON file not found: {args.json_file}")
        return
    
    try:
        # Initialize uploader
        uploader = QdrantUploader(config)
        
        # Create collection with appropriate vector size
        vector_size = config.get('vector_size', 1536)
        uploader.create_collection(vector_size=vector_size, recreate=config.get('recreate_collection', False))
        
        # Load JSON data
        data = uploader.load_json_data(args.json_file)
        
        if not data:
            logger.warning("No valid data found in JSON file")
            return
        
        # Upload to Qdrant
        uploaded_count = uploader.upload_to_qdrant(
            data, 
            batch_size=config.get('batch_size', 100)
        )
        
        # Display collection info
        collection_info = uploader.get_collection_info()
        logger.info(f"Collection info: {collection_info}")
        
        logger.info("Upload completed successfully!")
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

