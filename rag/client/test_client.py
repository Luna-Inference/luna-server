#!/usr/bin/env python3
"""
Simple test script for the RAG client
"""

import sys
import os

# Add the parent directory to the path so we can import the client
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_client import RAGClient

def test_client_basic():
    """Test basic client functionality"""
    print("Testing RAG Client...")
    
    # Create client
    client = RAGClient()
    
    # Test connection
    print("1. Testing connection...")
    status = client.get_status()
    if "error" in status:
        print("❌ Cannot connect to server")
        print("   Make sure the RAG server is running on http://localhost:1310")
        return False
    else:
        print("✅ Server connection successful")
    
    # Test version
    print("2. Testing version endpoint...")
    version = client.get_version()
    if "error" not in version:
        print(f"✅ Version: {version.get('version', 'unknown')}")
    else:
        print(f"❌ Version check failed: {version['error']}")
    
    # Test collections
    print("3. Testing collections endpoint...")
    collections = client.show_collections()
    if "error" not in collections:
        print(f"✅ Collections: {collections.get('collections', [])}")
    else:
        print(f"❌ Collections check failed: {collections['error']}")
    
    print("\n✅ Basic client tests completed!")
    return True

if __name__ == "__main__":
    test_client_basic() 