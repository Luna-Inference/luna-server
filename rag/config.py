"""
Configuration settings for the RAG server.
This file centralizes all configurable parameters to make them easier to manage.
"""

# ChromaDB Configuration
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
CHROMA_PERSIST_DIRECTORY = "./data"

# Server Configuration
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 1310
API_BASE_PATH = "/v1"
API_KEY = "anything"  # Default API key for authentication (can be any string)

# RAG Parameters
DEFAULT_COLLECTION_NAME = "default"
MAX_RESULTS = 5  # Default number of results to return for queries
DEFAULT_DISTANCE_THRESHOLD = 1.0  # Maximum distance for similarity search

# Debug Configuration
DEBUG_MODE = False
LOG_LEVEL = 2  # 0: Error, 1: Warning, 2: Info, 3: Debug

# Response Configuration
DEFAULT_RESPONSE_FORMAT = "json"  # json or text
ENABLE_METADATA = True  # Whether to include metadata in responses 