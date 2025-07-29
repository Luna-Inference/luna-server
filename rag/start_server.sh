#!/bin/bash

# RAG Server Startup Script

echo "Starting RAG Server..."

# Start the RAG server (will automatically start ChromaDB)
echo "Starting RAG server on port 1310..."
echo "ChromaDB will be started automatically if not already running."
python server.py --debug

echo "RAG server stopped." 