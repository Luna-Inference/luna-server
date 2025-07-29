# RAG Server

A REST API server for managing document collections and performing similarity search using ChromaDB.

## Overview

The RAG (Retrieval-Augmented Generation) server provides a simple HTTP API for:
- Adding documents to collections
- Querying documents using semantic similarity
- Managing collections and documents
- Health monitoring and status checking

## Features

- **Document Management**: Add, view, and remove documents from collections
- **Semantic Search**: Query documents using ChromaDB's embedding-based similarity search
- **Collection Management**: Create and manage multiple document collections
- **RESTful API**: Clean HTTP endpoints following REST principles
- **Error Handling**: Comprehensive error responses with proper HTTP status codes
- **Health Monitoring**: Built-in health check and status endpoints

## Prerequisites

- Python 3.7+
- ChromaDB server running
- Required Python packages (see `requirements.txt`)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the RAG server (ChromaDB will be started automatically):
```bash
python server.py
```

**Note**: The server will automatically start ChromaDB if it's not already running. If you prefer to manage ChromaDB separately, use the `--no_auto_chroma` flag:

```bash
python server.py --no_auto_chroma
```

## Configuration

The server can be configured by modifying `config.py` or using command-line arguments:

```bash
python server.py --chroma_host localhost --chroma_port 8000 --port 1310 --debug
```

### Command Line Options

- `--chroma_host`: ChromaDB server host (default: localhost)
- `--chroma_port`: ChromaDB server port (default: 8000)
- `--port`: RAG server port (default: 1310)
- `--debug`: Enable debug mode
- `--no_auto_chroma`: Do not automatically start ChromaDB server

### Configuration Options

- `CHROMA_HOST`: ChromaDB server host (default: localhost)
- `CHROMA_PORT`: ChromaDB server port (default: 8000)
- `SERVER_PORT`: RAG server port (default: 1310)
- `DEFAULT_COLLECTION_NAME`: Default collection name (default: "default")
- `MAX_RESULTS`: Maximum number of results for queries (default: 10)

## API Endpoints

### 1. Add Document
- **POST** `/add`
- Add a document to a collection

### 2. Show Collections
- **GET** `/show`
- List all available collections

### 3. View Collection
- **POST** `/view`
- View all documents in a collection

### 4. Remove Document
- **POST** `/remove`
- Remove a document from a collection

### 5. Query Documents
- **POST** `/query`
- Perform similarity search on documents

### 6. Status
- **GET** `/status`
- Get server status and connection info

### 7. Health Check
- **GET** `/health`
- Health check endpoint

### 8. Version
- **GET** `/version`
- Get application version

For detailed API documentation, see [server.md](server.md).

## Usage Examples

### Starting the Server

```bash
# Start RAG server (ChromaDB will be started automatically)
python server.py

# Or with debug mode
python server.py --debug

# If ChromaDB is already running elsewhere
python server.py --no_auto_chroma

# Using the startup script
./start_server.sh
```

### Adding Documents

```bash
curl -X POST http://localhost:1310/add \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is a document about machine learning",
    "collection": "ml_docs",
    "id": "doc_001"
  }'
```

### Querying Documents

```bash
curl -X POST http://localhost:1310/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "collection": "ml_docs",
    "n_results": 5
  }'
```

### Checking Server Status

```bash
curl http://localhost:1310/status
```

## Testing

Run the test suite to verify the server functionality:

```bash
python test_server.py
```

This will test all endpoints and demonstrate the server's capabilities.



## Error Handling

The server returns consistent error responses in JSON format:

```json
{
  "error": {
    "message": "Description of the error",
    "type": "error_type",
    "param": "parameter_name"
  }
}
```

Common error types:
- `invalid_request_error`: Invalid request parameters
- `not_found`: Resource not found
- `server_error`: Internal server error

## Development

### Project Structure

```
rag/
├── server.py          # Main server application
├── config.py          # Configuration settings
├── server.md          # API documentation
├── test_server.py     # Test suite
├── requirements.txt   # Python dependencies
├── README.md         # This file
└── data/             # ChromaDB data directory
```

### Adding New Features

1. Add new endpoints to `server.py`
2. Update `server.md` with API documentation
3. Add tests to `test_server.py`
4. Update configuration in `config.py` if needed

## Troubleshooting

### Common Issues

1. **ChromaDB Connection Failed**
   - The server will automatically start ChromaDB if it's not running
   - If auto-start fails, check if ChromaDB is installed: `pip install chromadb`
   - Check host and port configuration
   - Verify network connectivity

2. **Port Already in Use**
   - Change the server port in config.py
   - Or use `--port` command-line argument

3. **Permission Errors**
   - Ensure proper permissions for data directory
   - Check ChromaDB server permissions

### Logs

Enable debug mode for detailed logging:

```bash
python server.py --debug
```

## License

This project follows the same license as the parent repository.

## Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass 