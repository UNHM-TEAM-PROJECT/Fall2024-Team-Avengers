from  qdrant_client import QdrantClient, models

client = QdrantClient(host="localhost")

client.create_collection(collection_name = "internship2024", vectors_config = models.VectorParams(size=384, distance=models.Distance.DOT) )

