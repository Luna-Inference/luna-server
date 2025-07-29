#!/usr/bin/env python3
"""
Test script for the RAG server.
This script demonstrates how to use all the RAG server endpoints.
"""

import requests
import json
import time

# Server configuration
SERVER_URL = "http://localhost:1310"
TEST_COLLECTION = "test_collection"

def test_add_document():
    """Test adding documents to a collection"""
    print("=== Testing Add Document ===")
    
    # Test data
    documents = [
        {
            "content": "This is a document about machine learning and artificial intelligence.",
            "collection": TEST_COLLECTION,
            "id": "doc_ml_1"
        },
        {
            "content": "Python is a popular programming language for data science.",
            "collection": TEST_COLLECTION,
            "id": "doc_python_1"
        },
        {
            "content": "ChromaDB is a vector database for building AI applications.",
            "collection": TEST_COLLECTION,
            "id": "doc_chroma_1"
        }
    ]
    
    for doc in documents:
        response = requests.post(f"{SERVER_URL}/add", json=doc)
        print(f"Adding document {doc['id']}: {response.status_code}")
        if response.status_code == 200:
            print(f"  Success: {response.json()}")
        else:
            print(f"  Error: {response.json()}")
        print()

def test_show_collections():
    """Test listing all collections"""
    print("=== Testing Show Collections ===")
    
    response = requests.get(f"{SERVER_URL}/show")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Collections: {data['collections']}")
        print(f"Count: {data['count']}")
    else:
        print(f"Error: {response.json()}")
    print()

def test_view_collection():
    """Test viewing documents in a collection"""
    print("=== Testing View Collection ===")
    
    response = requests.post(f"{SERVER_URL}/view", json={"collection": TEST_COLLECTION})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Collection: {data['collection']}")
        print(f"Document count: {data['count']}")
        for doc in data['documents']:
            print(f"  ID: {doc['id']}")
            print(f"  Content: {doc['content'][:50]}...")
            print()
    else:
        print(f"Error: {response.json()}")
    print()

def test_query_documents():
    """Test querying documents"""
    print("=== Testing Query Documents ===")
    
    queries = [
        "What is machine learning?",
        "Tell me about Python programming",
        "What is ChromaDB used for?"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        response = requests.post(f"{SERVER_URL}/query", json={
            "query": query,
            "collection": TEST_COLLECTION,
            "n_results": 2
        })
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data['count']} results:")
            for result in data['results']:
                print(f"  ID: {result['id']}")
                print(f"  Distance: {result['distance']:.3f}")
                print(f"  Content: {result['content'][:50]}...")
                print()
        else:
            print(f"Error: {response.json()}")
        print()

def test_remove_document():
    """Test removing a document"""
    print("=== Testing Remove Document ===")
    
    doc_id = "doc_ml_1"
    response = requests.post(f"{SERVER_URL}/remove", json={
        "id": doc_id,
        "collection": TEST_COLLECTION
    })
    
    print(f"Removing document {doc_id}: {response.status_code}")
    if response.status_code == 200:
        print(f"Success: {response.json()}")
    else:
        print(f"Error: {response.json()}")
    print()

def test_status():
    """Test server status"""
    print("=== Testing Server Status ===")
    
    response = requests.get(f"{SERVER_URL}/status")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Server status: {data['status']}")
        print(f"Chroma connected: {data['chroma_connected']}")
        print(f"Collections: {data['collections']}")
    else:
        print(f"Error: {response.json()}")
    print()

def test_version():
    """Test version endpoint"""
    print("=== Testing Version ===")
    
    response = requests.get(f"{SERVER_URL}/version")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Version: {data['version']}")
    else:
        print(f"Error: {response.json()}")
    print()

def main():
    """Run all tests"""
    print("RAG Server Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{SERVER_URL}/status", timeout=5)
        if response.status_code != 200:
            print("Error: Server is not responding properly")
            return
    except requests.exceptions.RequestException as e:
        print(f"Error: Cannot connect to server at {SERVER_URL}")
        print(f"Make sure the RAG server is running on port 1310")
        return
    
    # Run tests
    test_status()
    test_version()
    test_show_collections()
    test_add_document()
    test_show_collections()
    test_view_collection()
    test_query_documents()
    test_remove_document()
    test_view_collection()  # Check that document was removed
    
    print("Test suite completed!")

if __name__ == "__main__":
    main() 