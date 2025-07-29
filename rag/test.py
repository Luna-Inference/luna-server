import chromadb
# chroma run --path data
chroma_client = chromadb.HttpClient(host='localhost', port=8000)
collection = chroma_client.get_or_create_collection(name="my_collection")
collection.add(
    ids=["id1", "id4"],
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ]
)
print(collection.get())
# {'ids': ['id3', 'id4', 'id1', 'id2'], 'embeddings': None, 'metadatas': [None, None, None, None], 'documents': ['This is a document about pineapple', 'This is a document about oranges', 'This is a document about pineapple', 'This is a document about oranges'], 'data': None, 'uris': None, 'included': ['metadatas', 'documents']}

results = collection.query(
    query_texts=["This is a query document about hawaii"], # Chroma will embed this for you
    n_results=2 # how many results to return
)
print(results)
# {'ids': [['id3', 'id1']], 'distances': [[1.0404011, 1.0404011]], 'embeddings': None, 'metadatas': [[None, None]], 'documents': [['This is a document about pineapple', 'This is a document about pineapple']], 'uris': None, 'data': None, 'included': ['metadatas', 'documents', 'distances']}

