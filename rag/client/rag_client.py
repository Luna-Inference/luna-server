#!/usr/bin/env python3
"""
RAG Client - A simple client to test all RAG server functionalities
"""

import requests
import json
import time
import sys
from typing import Dict, List, Any, Optional

class RAGClient:
    """Client for interacting with the RAG server"""
    
    def __init__(self, base_url: str = "http://localhost:1310"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to the server"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {"error": str(e)}
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            return {"error": "Invalid JSON response"}
    
    def add_document(self, content: str, collection: str = "default", doc_id: Optional[str] = None) -> Dict:
        """Add a document to a collection"""
        data = {
            "content": content,
            "collection": collection
        }
        if doc_id:
            data["id"] = doc_id
        
        return self._make_request("POST", "/add", data)
    
    def show_collections(self) -> Dict:
        """List all collections"""
        return self._make_request("GET", "/show")
    
    def view_collection(self, collection: str = "default") -> Dict:
        """View all documents in a collection"""
        return self._make_request("POST", "/view", {"collection": collection})
    
    def remove_document(self, doc_id: str, collection: str = "default") -> Dict:
        """Remove a document from a collection"""
        return self._make_request("POST", "/remove", {
            "id": doc_id,
            "collection": collection
        })
    
    def query_documents(self, query: str, collection: str = "default", n_results: int = 5) -> Dict:
        """Query documents in a collection"""
        return self._make_request("POST", "/query", {
            "query": query,
            "collection": collection,
            "n_results": n_results
        })
    
    def get_status(self) -> Dict:
        """Get server status"""
        return self._make_request("GET", "/status")
    
    def get_health(self) -> Dict:
        """Get health check"""
        return self._make_request("GET", "/health")
    
    def get_version(self) -> Dict:
        """Get server version"""
        return self._make_request("GET", "/version")

class RAGClientCLI:
    """Command-line interface for the RAG client"""
    
    def __init__(self):
        self.client = RAGClient()
        self.current_collection = "default"
    
    def print_response(self, response: Dict, title: str = ""):
        """Pretty print a response"""
        if title:
            print(f"\n=== {title} ===")
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            print("✅ Success!")
            print(json.dumps(response, indent=2, ensure_ascii=False))
    
    def test_connection(self):
        """Test server connection"""
        print("Testing server connection...")
        response = self.client.get_status()
        if "error" not in response:
            print("✅ Server is running and accessible")
            print(f"   Status: {response.get('status', 'unknown')}")
            print(f"   ChromaDB: {response.get('chroma_status', 'unknown')}")
        else:
            print("❌ Cannot connect to server")
            print("   Make sure the RAG server is running on http://localhost:1310")
    
    def interactive_menu(self):
        """Interactive menu for testing"""
        while True:
            print(f"\n{'='*50}")
            print("RAG Client - Interactive Menu")
            print(f"{'='*50}")
            print(f"Current collection: {self.current_collection}")
            print(f"Server: {self.client.base_url}")
            print()
            print("1. Test Connection")
            print("2. Add Document")
            print("3. Show Collections")
            print("4. View Collection")
            print("5. Query Documents")
            print("6. Remove Document")
            print("7. Server Status")
            print("8. Change Collection")
            print("9. Run Demo")
            print("0. Exit")
            print()
            
            choice = input("Enter your choice (0-9): ").strip()
            
            if choice == "0":
                print("Goodbye!")
                break
            elif choice == "1":
                self.test_connection()
            elif choice == "2":
                self.add_document_interactive()
            elif choice == "3":
                self.show_collections_interactive()
            elif choice == "4":
                self.view_collection_interactive()
            elif choice == "5":
                self.query_documents_interactive()
            elif choice == "6":
                self.remove_document_interactive()
            elif choice == "7":
                self.server_status_interactive()
            elif choice == "8":
                self.change_collection_interactive()
            elif choice == "9":
                self.run_demo()
            else:
                print("Invalid choice. Please try again.")
    
    def add_document_interactive(self):
        """Interactive document addition"""
        print("\n=== Add Document ===")
        content = input("Enter document content: ").strip()
        if not content:
            print("Content cannot be empty")
            return
        
        collection = input(f"Enter collection name (default: {self.current_collection}): ").strip()
        if not collection:
            collection = self.current_collection
        
        doc_id = input("Enter document ID (optional, press Enter to auto-generate): ").strip()
        if not doc_id:
            doc_id = None
        
        response = self.client.add_document(content, collection, doc_id)
        self.print_response(response, "Add Document Result")
    
    def show_collections_interactive(self):
        """Interactive collection listing"""
        response = self.client.show_collections()
        self.print_response(response, "Collections")
    
    def view_collection_interactive(self):
        """Interactive collection viewing"""
        collection = input(f"Enter collection name (default: {self.current_collection}): ").strip()
        if not collection:
            collection = self.current_collection
        
        response = self.client.view_collection(collection)
        self.print_response(response, f"Collection: {collection}")
    
    def query_documents_interactive(self):
        """Interactive document querying"""
        print("\n=== Query Documents ===")
        query = input("Enter search query: ").strip()
        if not query:
            print("Query cannot be empty")
            return
        
        collection = input(f"Enter collection name (default: {self.current_collection}): ").strip()
        if not collection:
            collection = self.current_collection
        
        n_results = input("Enter number of results (default: 5): ").strip()
        try:
            n_results = int(n_results) if n_results else 5
        except ValueError:
            n_results = 5
        
        response = self.client.query_documents(query, collection, n_results)
        self.print_response(response, "Query Results")
    
    def remove_document_interactive(self):
        """Interactive document removal"""
        print("\n=== Remove Document ===")
        doc_id = input("Enter document ID to remove: ").strip()
        if not doc_id:
            print("Document ID cannot be empty")
            return
        
        collection = input(f"Enter collection name (default: {self.current_collection}): ").strip()
        if not collection:
            collection = self.current_collection
        
        response = self.client.remove_document(doc_id, collection)
        self.print_response(response, "Remove Document Result")
    
    def server_status_interactive(self):
        """Interactive server status"""
        response = self.client.get_status()
        self.print_response(response, "Server Status")
    
    def change_collection_interactive(self):
        """Interactive collection change"""
        new_collection = input("Enter new collection name: ").strip()
        if new_collection:
            self.current_collection = new_collection
            print(f"Current collection changed to: {self.current_collection}")
        else:
            print("Collection name cannot be empty")
    
    def run_demo(self):
        """Run a complete demo of all functionalities"""
        print("\n" + "="*60)
        print("RAG Client Demo - Testing All Functionalities")
        print("="*60)
        
        # Test connection
        print("\n1. Testing server connection...")
        status = self.client.get_status()
        if "error" in status:
            print("❌ Cannot connect to server. Please start the RAG server first.")
            return
        print("✅ Server connection successful")
        
        # Demo collection
        demo_collection = "demo_collection"
        
        # Add documents
        print(f"\n2. Adding documents to '{demo_collection}'...")
        documents = [
            {
                "content": "Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.",
                "id": "doc_ml_1"
            },
            {
                "content": "Python is a high-level programming language known for its simplicity and readability.",
                "id": "doc_python_1"
            },
            {
                "content": "ChromaDB is a vector database designed for building AI applications with embeddings.",
                "id": "doc_chroma_1"
            },
            {
                "content": "Natural language processing (NLP) is a field of AI that focuses on the interaction between computers and human language.",
                "id": "doc_nlp_1"
            }
        ]
        
        for doc in documents:
            response = self.client.add_document(doc["content"], demo_collection, doc["id"])
            if "error" not in response:
                print(f"   ✅ Added: {doc['id']}")
            else:
                print(f"   ❌ Failed to add: {doc['id']} - {response['error']}")
        
        # Show collections
        print(f"\n3. Listing all collections...")
        response = self.client.show_collections()
        if "error" not in response:
            print(f"   Collections: {response.get('collections', [])}")
        
        # View collection
        print(f"\n4. Viewing documents in '{demo_collection}'...")
        response = self.client.view_collection(demo_collection)
        if "error" not in response:
            print(f"   Found {response.get('count', 0)} documents")
            for doc in response.get('documents', []):
                print(f"   - {doc['id']}: {doc['content'][:50]}...")
        
        # Query documents
        print(f"\n5. Testing queries...")
        queries = [
            "What is machine learning?",
            "Tell me about Python programming",
            "What is ChromaDB?",
            "Explain natural language processing"
        ]
        
        for query in queries:
            print(f"\n   Query: '{query}'")
            response = self.client.query_documents(query, demo_collection, 2)
            if "error" not in response:
                results = response.get('results', [])
                print(f"   Found {len(results)} results:")
                for result in results:
                    print(f"     - {result['id']} (distance: {result['distance']:.3f})")
                    print(f"       {result['content'][:60]}...")
            else:
                print(f"   ❌ Query failed: {response['error']}")
        
        # Remove a document
        print(f"\n6. Removing a document...")
        response = self.client.remove_document("doc_ml_1", demo_collection)
        if "error" not in response:
            print("   ✅ Document removed successfully")
        else:
            print(f"   ❌ Failed to remove document: {response['error']}")
        
        # Verify removal
        print(f"\n7. Verifying document removal...")
        response = self.client.view_collection(demo_collection)
        if "error" not in response:
            print(f"   Remaining documents: {response.get('count', 0)}")
        
        # Server info
        print(f"\n8. Server information...")
        version = self.client.get_version()
        if "error" not in version:
            print(f"   Version: {version.get('version', 'unknown')}")
        
        print(f"\n{'='*60}")
        print("Demo completed successfully!")
        print("="*60)

def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Command line mode
        client = RAGClient()
        command = sys.argv[1].lower()
        
        if command == "status":
            response = client.get_status()
            print(json.dumps(response, indent=2))
        elif command == "demo":
            cli = RAGClientCLI()
            cli.run_demo()
        elif command == "add" and len(sys.argv) >= 4:
            content = sys.argv[2]
            collection = sys.argv[3] if len(sys.argv) > 3 else "default"
            response = client.add_document(content, collection)
            print(json.dumps(response, indent=2))
        elif command == "query" and len(sys.argv) >= 3:
            query = sys.argv[2]
            collection = sys.argv[3] if len(sys.argv) > 3 else "default"
            response = client.query_documents(query, collection)
            print(json.dumps(response, indent=2))
        else:
            print("Usage:")
            print("  python rag_client.py status")
            print("  python rag_client.py demo")
            print("  python rag_client.py add 'content' [collection]")
            print("  python rag_client.py query 'query' [collection]")
    else:
        # Interactive mode
        cli = RAGClientCLI()
        cli.interactive_menu()

if __name__ == "__main__":
    main() 