#!/usr/bin/env python3
"""
Test script for Qdrant upload functionality.
Creates a small test dataset and uploads it to verify the setup.
"""

import json
import tempfile
import os
from upload_to_qdrant import QdrantUploader

def create_test_data():
    """Create a small test dataset for testing."""
    test_data = [
        {
            "text": "Cognitive Behavioral Therapy (CBT) is a form of psychotherapy.",
            "source_file": "test.md",
            "chapter_name": "Introduction",
            "section_name": "What is CBT?",
            "subsection_name": None
        },
        {
            "text": "CBT focuses on changing unhelpful thoughts and behaviors.",
            "source_file": "test.md",
            "chapter_name": "Introduction",
            "section_name": "Core Principles",
            "subsection_name": "Thought Patterns"
        },
        {
            "text": "Mindfulness is a key component of modern CBT approaches.",
            "source_file": "test.md",
            "chapter_name": "Techniques",
            "section_name": "Mindfulness",
            "subsection_name": "Basic Practice"
        }
    ]
    return test_data

def test_upload():
    """Test the upload functionality with a small dataset."""
    print("🧪 Testing Qdrant upload functionality...")
    
    # Create test configuration
    config = {
        'qdrant_host': 'https://75f5cc60-af58-46dd-8e92-16ff874b8b8c.us-east4-0.gcp.cloud.qdrant.io',
        'qdrant_port': 6333,
        'qdrant_api_key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.RQmW_5jzMpwqbws5PnYFwW7hh0FFW6AejFLKNNHYfAs',
        'collection_name': 'test_collection',
        'embedding_model': 'text-embedding-3-small',
        'vector_size': 1536,
        'batch_size': 10,
        'recreate_collection': True
    }
    
    try:
        # Create test data
        test_data = create_test_data()
        print(f"✅ Created test dataset with {len(test_data)} entries")
        
        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f, indent=2)
            temp_file = f.name
        
        print(f"✅ Created temporary test file: {temp_file}")
        
        # Initialize uploader
        print("🔌 Initializing Qdrant uploader...")
        uploader = QdrantUploader(config)
        print("✅ Uploader initialized successfully")
        
        # Create collection
        print("📚 Creating test collection...")
        vector_size = config.get('vector_size', 1536)
        uploader.create_collection(vector_size=vector_size, recreate=True)
        print("✅ Collection created successfully")
        
        # Upload test data
        print("📤 Uploading test data...")
        uploaded_count = uploader.upload_to_qdrant(test_data, batch_size=10)
        print(f"✅ Successfully uploaded {uploaded_count} points")
        
        # Get collection info
        collection_info = uploader.get_collection_info()
        print(f"📊 Collection info: {collection_info}")
        
        print("\n🎉 All tests passed! Your Qdrant setup is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check that all dependencies are installed (pip install -r requirements.txt)")
        print("2. Set your OpenAI API key: export OPENAI_API_KEY=your_api_key_here")
        print("3. Verify your Qdrant Cloud API key is valid")
        print("4. Check network connectivity to Qdrant Cloud")
        return False
    
    finally:
        # Clean up temporary file
        if 'temp_file' in locals():
            try:
                os.unlink(temp_file)
                print(f"🧹 Cleaned up temporary file: {temp_file}")
            except:
                pass
    
    return True

if __name__ == "__main__":
    success = test_upload()
    exit(0 if success else 1)

