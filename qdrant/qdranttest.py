"""
This script demonstrates how to use the Qdrant vector database for embedding and 
retrieving text. It adds sample documents, generates embeddings, stores them in a 
test collection, and performs a search query to retrieve relevant results.

Modules Used:
- QdrantClient: For connecting to and managing the Qdrant database.
- TextEmbedding: For generating embeddings from text data.
- os: For managing file paths.
"""

import os
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding

# Sample documents to store in the Qdrant database
docs = [
    "The internship class requires 80 on field hours",
    "On field hours may be remote or in person"
]

# Define the storage path for Qdrant data (if needed)
exec_path = os.path.dirname(__file__)
store_path = os.path.join(exec_path, "qdrant_data")

# Initialize the Qdrant client
client = QdrantClient(host='localhost')

# Initialize the embedding model
embed_model = TextEmbedding()

# Generate embeddings for the sample documents
embeds = embed_model.embed(docs)

# Create a batch of embeddings with IDs and payloads
embeds = models.Batch(
    ids=[1, 2],  # Unique IDs for the documents
    vectors=list(embeds),  # Embedding vectors for the documents
    payloads=[{"1": docs[0]}, {"2": docs[1]}]  # Payloads containing document content
)

# Uncomment the following block to create a new collection (if not already created)
# client.create_collection(
#     collection_name="test_collection2",
#     vectors_config=models.VectorParams(size=384, distance=models.Distance.DOT)
# )

# Upsert the embeddings into the "test_collection2" collection
client.upsert(
    collection_name="test_collection2",
    points=embeds
)

# Perform a search query in the collection
search_result = client.search(
    collection_name="test_collection2",
    query_vector=next(embed_model.embed(["How many hours do I need"]))  # Query text
)

# Print the search results
print(search_result)

# Close the Qdrant client connection
client.close()
