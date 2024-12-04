"""
This module provides a function to search a Qdrant vector database using 
an embedding model. It is designed to handle natural language queries 
and return the most relevant results from the specified collection.

Modules Used:
- QdrantClient: For interacting with the Qdrant vector database.
- TextEmbedding: For generating embeddings from text queries.
"""

from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding

def search_db(client, q_text, embed_model, collection_name="internship2024"):
    """
    Queries the Qdrant vector database and retrieves the most relevant results.

    Args:
        client (QdrantClient): The Qdrant client used to connect to the database.
        q_text (str): The natural language query to search for.
        embed_model (TextEmbedding): The embedding model to convert the query into a vector.
        collection_name (str, optional): The name of the collection in the database. Defaults to "internship2024".

    Returns:
        list[models.models]: A list of search results from the Qdrant database.
    """
    # Generate the embedding for the query and search the Qdrant database
    search_result = client.search(
        collection_name=collection_name,
        limit=15,  # Limit the results to 15 entries
        query_vector=next(embed_model.embed([q_text]))  # Convert query to a vector
    )
    return search_result

if __name__ == "__main__":
    """
    Main block for standalone execution. Demonstrates how to perform a search query 
    against a Qdrant vector database and print the first result's payload values.
    """
    client = QdrantClient(host='localhost')  # Initialize Qdrant client
    embed_model = TextEmbedding()  # Initialize the embedding model
    result = search_db(client, "What is the schedule for week 4", embed_model)  # Perform a search query
    print(result[0].payload.values())  # Print the values of the first result's payload
