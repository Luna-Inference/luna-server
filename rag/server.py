import os
import sys
import json
import uuid
import argparse
import threading
import time
import subprocess
import signal
import atexit
from datetime import datetime
from typing import List, Dict, Any, Optional

import chromadb
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from config import *

app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True,
        "max_age": 3600
    }
})

# Global ChromaDB client and process
chroma_client = None
collections_cache = {}
chroma_process = None

def openai_error_response(message, error_type="invalid_request_error", param=None, code=None, status_code=400):
    """Generate OpenAI-compatible error response"""
    return jsonify({
        "error": {
            "message": message,
            "type": error_type,
            "param": param,
            "code": code
        }
    }), status_code

def start_chroma_server():
    """Start ChromaDB server as a subprocess"""
    global chroma_process
    
    try:
        # Check if ChromaDB is already running
        try:
            test_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
            test_client.heartbeat()
            print(f"ChromaDB is already running on {CHROMA_HOST}:{CHROMA_PORT}")
            return True
        except:
            pass  # ChromaDB is not running, continue to start it
        
        # Create data directory if it doesn't exist
        os.makedirs(CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        
        # Start ChromaDB server
        print(f"Starting ChromaDB server on {CHROMA_HOST}:{CHROMA_PORT}...")
        chroma_process = subprocess.Popen(
            ["chroma", "run", "--path", CHROMA_PERSIST_DIRECTORY, "--host", CHROMA_HOST, "--port", str(CHROMA_PORT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for ChromaDB to start
        time.sleep(3)
        
        # Test connection
        max_retries = 10
        for i in range(max_retries):
            try:
                test_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
                test_client.heartbeat()
                print(f"✅ ChromaDB server started successfully on {CHROMA_HOST}:{CHROMA_PORT}")
                return True
            except Exception as e:
                if i < max_retries - 1:
                    print(f"Waiting for ChromaDB to start... (attempt {i+1}/{max_retries})")
                    time.sleep(2)
                else:
                    print(f"❌ Failed to start ChromaDB server: {e}")
                    return False
                    
    except Exception as e:
        print(f"❌ Error starting ChromaDB server: {e}")
        return False

def stop_chroma_server():
    """Stop ChromaDB server subprocess"""
    global chroma_process
    
    if chroma_process:
        print("Stopping ChromaDB server...")
        try:
            chroma_process.terminate()
            chroma_process.wait(timeout=5)
            print("✅ ChromaDB server stopped")
        except subprocess.TimeoutExpired:
            print("⚠️  ChromaDB server didn't stop gracefully, forcing...")
            chroma_process.kill()
            chroma_process.wait()
        except Exception as e:
            print(f"❌ Error stopping ChromaDB server: {e}")

def cleanup_on_exit():
    """Cleanup function called on exit"""
    stop_chroma_server()

# Register cleanup function
atexit.register(cleanup_on_exit)

def initialize_chroma_client():
    """Initialize ChromaDB client"""
    global chroma_client
    try:
        chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        # Test connection
        chroma_client.heartbeat()
        print(f"Connected to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT}")
        return True
    except Exception as e:
        print(f"Failed to connect to ChromaDB: {e}")
        return False

def get_collection(collection_name: str):
    """Get or create a collection"""
    global chroma_client, collections_cache
    
    if collection_name not in collections_cache:
        try:
            collections_cache[collection_name] = chroma_client.get_or_create_collection(name=collection_name)
        except Exception as e:
            print(f"Error getting collection {collection_name}: {e}")
            return None
    
    return collections_cache[collection_name]

def validate_collection_name(collection_name: str) -> bool:
    """Validate collection name"""
    if not collection_name or not isinstance(collection_name, str):
        return False
    if len(collection_name) > 100:  # Reasonable limit
        return False
    # Add more validation as needed
    return True

def validate_document_id(document_id: str) -> bool:
    """Validate document ID"""
    if not document_id or not isinstance(document_id, str):
        return False
    if len(document_id) > 200:  # Reasonable limit
        return False
    return True

# RAG API Endpoints

@app.route('/add', methods=['POST'])
def add_document():
    """Add a document to a collection"""
    try:
        data = request.json
        if not data:
            return openai_error_response("Missing JSON body")
        
        # Validate required fields
        if 'content' not in data:
            return openai_error_response("Missing required parameter: content", param="content")
        
        content = data['content']
        if not isinstance(content, str) or not content.strip():
            return openai_error_response("Content must be a non-empty string", param="content")
        
        collection_name = data.get('collection', DEFAULT_COLLECTION_NAME)
        if not validate_collection_name(collection_name):
            return openai_error_response("Invalid collection name", param="collection")
        
        # Generate document ID if not provided
        document_id = data.get('id', f"doc_{str(uuid.uuid4())}")
        if not validate_document_id(document_id):
            return openai_error_response("Invalid document ID", param="id")
        
        # Get collection
        collection = get_collection(collection_name)
        if not collection:
            return openai_error_response("Failed to get collection", error_type="server_error", status_code=500)
        
        # Add document
        try:
            collection.add(
                ids=[document_id],
                documents=[content],
                metadatas=[{"added_at": datetime.now().isoformat()}] if ENABLE_METADATA else None
            )
            
            response = {
                "status": "success",
                "message": f"Document added successfully to collection '{collection_name}'",
                "document_id": document_id,
                "collection": collection_name
            }
            return jsonify(response), 200
            
        except Exception as e:
            return openai_error_response(f"Failed to add document: {str(e)}", error_type="server_error", status_code=500)
            
    except Exception as e:
        return openai_error_response(f"Internal server error: {str(e)}", error_type="server_error", status_code=500)

@app.route('/show', methods=['GET'])
def show_collections():
    """Show all collection names"""
    try:
        global chroma_client
        
        if not chroma_client:
            return openai_error_response("ChromaDB client not initialized", error_type="server_error", status_code=500)
        
        try:
            collections = chroma_client.list_collections()
            collection_names = [col.name for col in collections]
            
            response = {
                "status": "success",
                "collections": collection_names,
                "count": len(collection_names)
            }
            return jsonify(response), 200
            
        except Exception as e:
            return openai_error_response(f"Failed to list collections: {str(e)}", error_type="server_error", status_code=500)
            
    except Exception as e:
        return openai_error_response(f"Internal server error: {str(e)}", error_type="server_error", status_code=500)

@app.route('/view', methods=['POST'])
def view_collection():
    """View all records in a collection with id & string"""
    try:
        data = request.json
        if not data:
            return openai_error_response("Missing JSON body")
        
        collection_name = data.get('collection', DEFAULT_COLLECTION_NAME)
        if not validate_collection_name(collection_name):
            return openai_error_response("Invalid collection name", param="collection")
        
        # Get collection
        collection = get_collection(collection_name)
        if not collection:
            return openai_error_response("Failed to get collection", error_type="server_error", status_code=500)
        
        try:
            # Get all documents in collection
            results = collection.get()
            
            documents = []
            if results['ids']:
                for i, doc_id in enumerate(results['ids']):
                    doc_data = {
                        "id": doc_id,
                        "content": results['documents'][i] if results['documents'] else "",
                        "metadata": results['metadatas'][i] if results['metadatas'] else {}
                    }
                    documents.append(doc_data)
            
            response = {
                "status": "success",
                "collection": collection_name,
                "documents": documents,
                "count": len(documents)
            }
            return jsonify(response), 200
            
        except Exception as e:
            return openai_error_response(f"Failed to retrieve documents: {str(e)}", error_type="server_error", status_code=500)
            
    except Exception as e:
        return openai_error_response(f"Internal server error: {str(e)}", error_type="server_error", status_code=500)

@app.route('/remove', methods=['POST'])
def remove_document():
    """Remove a document from a collection"""
    try:
        data = request.json
        if not data:
            return openai_error_response("Missing JSON body")
        
        # Validate required fields
        if 'id' not in data:
            return openai_error_response("Missing required parameter: id", param="id")
        
        document_id = data['id']
        if not validate_document_id(document_id):
            return openai_error_response("Invalid document ID", param="id")
        
        collection_name = data.get('collection', DEFAULT_COLLECTION_NAME)
        if not validate_collection_name(collection_name):
            return openai_error_response("Invalid collection name", param="collection")
        
        # Get collection
        collection = get_collection(collection_name)
        if not collection:
            return openai_error_response("Failed to get collection", error_type="server_error", status_code=500)
        
        try:
            # Check if document exists
            existing = collection.get(ids=[document_id])
            if not existing['ids']:
                return openai_error_response(f"Document with ID '{document_id}' not found in collection '{collection_name}'", 
                                           error_type="not_found", status_code=404)
            
            # Remove document
            collection.delete(ids=[document_id])
            
            response = {
                "status": "success",
                "message": f"Document '{document_id}' removed successfully from collection '{collection_name}'",
                "document_id": document_id,
                "collection": collection_name
            }
            return jsonify(response), 200
            
        except Exception as e:
            return openai_error_response(f"Failed to remove document: {str(e)}", error_type="server_error", status_code=500)
            
    except Exception as e:
        return openai_error_response(f"Internal server error: {str(e)}", error_type="server_error", status_code=500)

@app.route('/query', methods=['POST'])
def query_documents():
    """Query documents in a collection"""
    try:
        data = request.json
        if not data:
            return openai_error_response("Missing JSON body")
        
        # Validate required fields
        if 'query' not in data:
            return openai_error_response("Missing required parameter: query", param="query")
        
        query_text = data['query']
        if not isinstance(query_text, str) or not query_text.strip():
            return openai_error_response("Query must be a non-empty string", param="query")
        
        collection_name = data.get('collection', DEFAULT_COLLECTION_NAME)
        if not validate_collection_name(collection_name):
            return openai_error_response("Invalid collection name", param="collection")
        
        n_results = data.get('n_results', MAX_RESULTS)
        if not isinstance(n_results, int) or n_results < 1:
            return openai_error_response("n_results must be a positive integer", param="n_results")
        
        # Get collection
        collection = get_collection(collection_name)
        if not collection:
            return openai_error_response("Failed to get collection", error_type="server_error", status_code=500)
        
        try:
            # Query documents
            results = collection.query(
                query_texts=[query_text],
                n_results=min(n_results, MAX_RESULTS)
            )
            
            # Format results
            documents = []
            if results['ids'] and results['ids'][0]:
                for i, doc_id in enumerate(results['ids'][0]):
                    doc_data = {
                        "id": doc_id,
                        "content": results['documents'][0][i] if results['documents'] and results['documents'][0] else "",
                        "distance": results['distances'][0][i] if results['distances'] and results['distances'][0] else None,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                    }
                    documents.append(doc_data)
            
            response = {
                "status": "success",
                "query": query_text,
                "collection": collection_name,
                "results": documents,
                "count": len(documents)
            }
            return jsonify(response), 200
            
        except Exception as e:
            return openai_error_response(f"Failed to query documents: {str(e)}", error_type="server_error", status_code=500)
            
    except Exception as e:
        return openai_error_response(f"Internal server error: {str(e)}", error_type="server_error", status_code=500)

@app.route('/status', methods=['GET'])
def get_status():
    """Get server status and statistics"""
    try:
        global chroma_client
        
        status_data = {
            "status": "healthy" if chroma_client else "unhealthy",
            "chroma_connected": chroma_client is not None,
            "chroma_host": CHROMA_HOST,
            "chroma_port": CHROMA_PORT,
            "collections_count": len(collections_cache),
            "collections": list(collections_cache.keys()),
            "server_timestamp": datetime.now().isoformat()
        }
        
        # Test ChromaDB connection if available
        if chroma_client:
            try:
                chroma_client.heartbeat()
                status_data["chroma_status"] = "connected"
            except Exception as e:
                status_data["chroma_status"] = f"error: {str(e)}"
                status_data["status"] = "unhealthy"
        else:
            status_data["chroma_status"] = "not_initialized"
        
        return jsonify(status_data), 200
        
    except Exception as e:
        return openai_error_response(f"Internal server error: {str(e)}", error_type="server_error", status_code=500)

# Health check endpoint (alias for status)
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return get_status()

# App version endpoint
@app.route('/version', methods=['GET'])
def get_version():
    """Get application version"""
    try:
        version_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'VERSION')
        with open(version_file, 'r') as f:
            version = f.read().strip()
        return jsonify({"version": version}), 200
    except:
        return jsonify({"version": "unknown"}), 200

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--chroma_host', type=str, default=CHROMA_HOST, help='ChromaDB host (default from config.py)')
    parser.add_argument('--chroma_port', type=int, default=CHROMA_PORT, help='ChromaDB port (default from config.py)')
    parser.add_argument('--port', type=int, default=SERVER_PORT, help='Port to run the server on (default from config.py)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--no_auto_chroma', action='store_true', help='Do not automatically start ChromaDB server')
    args = parser.parse_args()
    
    print(f"Using ChromaDB host: {args.chroma_host}")
    print(f"Using ChromaDB port: {args.chroma_port}")
    print(f"Using server port: {args.port}")
    
    # Start ChromaDB server if not disabled
    if not args.no_auto_chroma:
        print("=========Starting ChromaDB Server===========")
        if not start_chroma_server():
            print("Error: Failed to start ChromaDB server.")
            print("You can try running with --no_auto_chroma if ChromaDB is already running.")
            sys.exit(1)
    else:
        print("=========Using existing ChromaDB server===========")
    
    # Initialize ChromaDB client
    print("=========Initializing ChromaDB connection===========")
    if not initialize_chroma_client():
        print("Error: Failed to connect to ChromaDB. Please ensure ChromaDB is running.")
        sys.exit(1)
    
    print("ChromaDB connection established successfully!")
    print("RAG server is starting...")
    print(f"API Endpoints:")
    print(f"  POST /add - Add document to collection")
    print(f"  GET  /show - List all collections")
    print(f"  POST /view - View documents in collection")
    print(f"  POST /remove - Remove document from collection")
    print(f"  POST /query - Query documents")
    print(f"  GET  /status - Server status")
    print(f"  GET  /health - Health check")
    print("==============================")
    
    try:
        # Start the Flask application
        app.run(host=SERVER_HOST, port=args.port, threaded=True, debug=args.debug or DEBUG_MODE)
    except KeyboardInterrupt:
        print("\nReceived interrupt signal, shutting down...")
    finally:
        cleanup_on_exit() 