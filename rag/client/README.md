# RAG Client

A simple client to test all RAG server functionalities with both interactive and command-line interfaces.

## Features

- **Interactive Menu**: Easy-to-use menu-driven interface
- **Command Line**: Quick commands for automation
- **Demo Mode**: Complete demonstration of all server features
- **Error Handling**: Comprehensive error reporting
- **Pretty Output**: Formatted JSON responses

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure the RAG server is running on `http://localhost:1310`

## Usage

### Interactive Mode

Run the client without arguments to start the interactive menu:

```bash
python rag_client.py
```

This will show a menu with options to:
- Test server connection
- Add documents
- Show collections
- View collection contents
- Query documents
- Remove documents
- Check server status
- Change current collection
- Run complete demo

### Command Line Mode

Use specific commands for automation:

```bash
# Check server status
python rag_client.py status

# Run complete demo
python rag_client.py demo

# Add a document
python rag_client.py add "This is a test document" my_collection

# Query documents
python rag_client.py query "test query" my_collection
```

### Demo Mode

The demo mode tests all server functionalities:

1. **Connection Test**: Verifies server is accessible
2. **Document Addition**: Adds sample documents to a demo collection
3. **Collection Management**: Lists and views collections
4. **Query Testing**: Tests semantic search with various queries
5. **Document Removal**: Removes a document and verifies
6. **Server Info**: Displays version and status information

## Examples

### Interactive Session

```
==================================================
RAG Client - Interactive Menu
==================================================
Current collection: default
Server: http://localhost:1310

1. Test Connection
2. Add Document
3. Show Collections
4. View Collection
5. Query Documents
6. Remove Document
7. Server Status
8. Change Collection
9. Run Demo
0. Exit

Enter your choice (0-9): 9
```

### Adding a Document

```
=== Add Document ===
Enter document content: This is a document about machine learning
Enter collection name (default: default): ml_docs
Enter document ID (optional, press Enter to auto-generate): doc_001

=== Add Document Result ===
✅ Success!
{
  "status": "success",
  "message": "Document added successfully to collection 'ml_docs'",
  "document_id": "doc_001",
  "collection": "ml_docs"
}
```

### Querying Documents

```
=== Query Documents ===
Enter search query: What is machine learning?
Enter collection name (default: default): ml_docs
Enter number of results (default: 5): 3

=== Query Results ===
✅ Success!
{
  "status": "success",
  "query": "What is machine learning?",
  "collection": "ml_docs",
  "results": [
    {
      "id": "doc_001",
      "content": "This is a document about machine learning",
      "distance": 0.15,
      "metadata": {
        "added_at": "2024-01-15T10:30:00"
      }
    }
  ],
  "count": 1
}
```

## Error Handling

The client provides clear error messages for common issues:

- **Connection Errors**: When server is not running
- **Invalid Input**: When required parameters are missing
- **Server Errors**: When server returns error responses
- **Network Issues**: When requests timeout or fail

## Configuration

The client connects to `http://localhost:1310` by default. To change the server URL, modify the `base_url` parameter in the `RAGClient` class:

```python
client = RAGClient(base_url="http://your-server:1310")
```

## Troubleshooting

### Common Issues

1. **"Cannot connect to server"**
   - Ensure RAG server is running on port 1310
   - Check if ChromaDB is running on port 8000
   - Verify network connectivity

2. **"Invalid JSON response"**
   - Check server logs for errors
   - Verify server is responding correctly

3. **"Request failed"**
   - Check server status
   - Verify server configuration

### Debug Mode

For detailed debugging, you can modify the client to show more information:

```python
# Add this to see raw HTTP requests
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Integration

The `RAGClient` class can be imported and used in other Python scripts:

```python
from rag_client import RAGClient

client = RAGClient()
response = client.add_document("My document content", "my_collection")
print(response)
```

## License

This client follows the same license as the parent RAG server project. 