# API Endpoint Documentation for RAG server.py

This document provides details about the API endpoints available in the RAG server (`server.py`).

## Overview

The RAG server provides a REST API for managing document collections and performing similarity search using ChromaDB. The server runs on port 1310 by default and provides endpoints for adding, viewing, removing, and querying documents.

## 1. Add Document

- **Endpoint**: `/add`
- **Method**: `POST`
- **Description**: Add a document to a collection for later retrieval and similarity search.

- **Request Body (JSON)**:
    ```json
    {
        "content": "This is the document content to be added",
        "collection": "my_collection",  // Optional, defaults to "default"
        "id": "doc_123"                 // Optional, auto-generated if not provided
    }
    ```

- **Response (JSON)**:
    ```json
    {
        "status": "success",
        "message": "Document added successfully to collection 'my_collection'",
        "document_id": "doc_123",
        "collection": "my_collection"
    }
    ```

- **Error Response**:
    ```json
    {
        "error": {
            "message": "Content must be a non-empty string",
            "type": "invalid_request_error",
            "param": "content"
        }
    }
    ```

## 2. Show Collections

- **Endpoint**: `/show`
- **Method**: `GET`
- **Description**: List all available collections in the ChromaDB instance.

- **Request Body**: None

- **Response (JSON)**:
    ```json
    {
        "status": "success",
        "collections": ["default", "my_collection", "another_collection"],
        "count": 3
    }
    ```

## 3. View Collection

- **Endpoint**: `/view`
- **Method**: `POST`
- **Description**: View all documents in a specific collection with their IDs and content.

- **Request Body (JSON)**:
    ```json
    {
        "collection": "my_collection"  // Optional, defaults to "default"
    }
    ```

- **Response (JSON)**:
    ```json
    {
        "status": "success",
        "collection": "my_collection",
        "documents": [
            {
                "id": "doc_123",
                "content": "This is the document content",
                "metadata": {
                    "added_at": "2024-01-15T10:30:00"
                }
            },
            {
                "id": "doc_456",
                "content": "Another document content",
                "metadata": {
                    "added_at": "2024-01-15T11:00:00"
                }
            }
        ],
        "count": 2
    }
    ```

## 4. Remove Document

- **Endpoint**: `/remove`
- **Method**: `POST`
- **Description**: Remove a specific document from a collection.

- **Request Body (JSON)**:
    ```json
    {
        "id": "doc_123",
        "collection": "my_collection"  // Optional, defaults to "default"
    }
    ```

- **Response (JSON)**:
    ```json
    {
        "status": "success",
        "message": "Document 'doc_123' removed successfully from collection 'my_collection'",
        "document_id": "doc_123",
        "collection": "my_collection"
    }
    ```

- **Error Response (Document not found)**:
    ```json
    {
        "error": {
            "message": "Document with ID 'doc_123' not found in collection 'my_collection'",
            "type": "not_found"
        }
    }
    ```

## 5. Delete Collection

- **Endpoint**: `/delete_collection`
- **Method**: `POST`
- **Description**: Delete a collection and all its documents.

- **Request Body (JSON)**:
    ```json
    {
        "collection": "my_collection"  // Optional, defaults to "default"
    }
    ```

- **Response (JSON)**:
    ```json
    {
        "status": "success",
        "message": "Collection 'my_collection' deleted successfully",
        "collection": "my_collection"
    }
    ```

- **Error Response (Collection not found)**:
    ```json
    {
        "error": {
            "message": "Collection 'my_collection' not found",
            "type": "not_found"
        }
    }
    ```

## 6. Query Documents

- **Endpoint**: `/query`
- **Method**: `POST`
- **Description**: Perform similarity search on documents in a collection using semantic embeddings.

- **Request Body (JSON)**:
    ```json
    {
        "query": "What is the main topic?",
        "collection": "my_collection",  // Optional, defaults to "default"
        "n_results": 5                  // Optional, defaults to 10
    }
    ```

- **Response (JSON)**:
    ```json
    {
        "status": "success",
        "query": "What is the main topic?",
        "collection": "my_collection",
        "results": [
            {
                "id": "doc_123",
                "content": "This document discusses the main topic in detail",
                "distance": 0.15,
                "metadata": {
                    "added_at": "2024-01-15T10:30:00"
                }
            },
            {
                "id": "doc_456",
                "content": "Another document related to the topic",
                "distance": 0.25,
                "metadata": {
                    "added_at": "2024-01-15T11:00:00"
                }
            }
        ],
        "count": 2
    }
    ```

**Note**: The `distance` field indicates similarity - lower values mean more similar documents.

## 7. Status

- **Endpoint**: `/status`
- **Method**: `GET`
- **Description**: Get server status and connection information.

- **Request Body**: None

- **Response (JSON)**:
    ```json
    {
        "status": "healthy",
        "chroma_connected": true,
        "chroma_host": "localhost",
        "chroma_port": 8000,
        "collections_count": 2,
        "collections": ["default", "my_collection"],
        "chroma_status": "connected",
        "server_timestamp": "2024-01-15T12:00:00"
    }
    ```

## 8. Health Check

- **Endpoint**: `/health`
- **Method**: `GET`
- **Description**: Health check endpoint (alias for `/status`).

- **Request Body**: None

- **Response**: Same as `/status` endpoint.

## 9. Version

- **Endpoint**: `/version`
- **Method**: `GET`
- **Description**: Get application version.

- **Request Body**: None

- **Response (JSON)**:
    ```json
    {
        "version": "1.0.0"
    }
    ```

## Error Handling

All endpoints return consistent error responses in the following format:

```json
{
    "error": {
        "message": "Description of the error",
        "type": "error_type",
        "param": "parameter_name",  // Optional
        "code": "error_code"        // Optional
    }
}
```

Common error types:
- `invalid_request_error`: Invalid request parameters
- `not_found`: Resource not found
- `server_error`: Internal server error

## Configuration

The server can be configured using command-line arguments:

```bash
python server.py --chroma_host localhost --chroma_port 8000 --port 1310 --debug
```

Or by modifying the `config.py` file:
- `CHROMA_HOST`: ChromaDB server host (default: localhost)
- `CHROMA_PORT`: ChromaDB server port (default: 8000)
- `SERVER_PORT`: RAG server port (default: 1310)
- `DEFAULT_COLLECTION_NAME`: Default collection name (default: "default")
- `MAX_RESULTS`: Maximum number of results for queries (default: 10)

## Usage Examples

### Starting the server:
```bash
# Start ChromaDB first
chroma run --path data

# Start RAG server
python server.py
```

### Adding documents:
```bash
curl -X POST http://localhost:1310/add \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is a document about machine learning",
    "collection": "ml_docs"
  }'
```

### Querying documents:
```bash
curl -X POST http://localhost:1310/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "collection": "ml_docs",
    "n_results": 3
  }'
```

### Deleting a collection:
```bash
curl -X POST http://localhost:1310/delete_collection \
  -H "Content-Type: application/json" \
  -d '{
    "collection": "ml_docs"
  }'
```

### Checking server status:
```bash
curl http://localhost:1310/status
``` 