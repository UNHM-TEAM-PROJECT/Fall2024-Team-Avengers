"""
This script processes a PDF file, splits it into text chunks, and uploads these 
chunks into a Qdrant vector database. It requires the PDF file name and collection 
name as command-line arguments.

Modules Used:
- PyPDF2: For reading and extracting text from PDF files.
- QdrantClient: For interacting with the Qdrant vector database.
- TextEmbedding: For generating embeddings from text chunks.
- CharacterTextSplitter: For splitting large text into manageable chunks.
"""

import os
import sys
import PyPDF2
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
from langchain.text_splitter import CharacterTextSplitter

# Chunk size for splitting text
CHUNK_SIZE = 300

def get_docs(pdf_path):
    """
    Converts a PDF file into a single string of text.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""  # Extract text from each page
    return text

def path_from_name(file_name):
    """
    Constructs the full file path from the provided file name.

    Args:
        file_name (str): Name of the file.

    Returns:
        str: Full file path to the specified file.
    """
    exec_path = os.path.dirname(__file__)  # Get the directory of the script
    file_path = os.path.join(exec_path, file_name)  # Combine directory with file name
    return file_path

# Get file path and collection name from command-line arguments
path = path_from_name(sys.argv[1])
collect = sys.argv[2]

# Extract text from the PDF
docs = get_docs(path)

# Initialize the text splitter for chunking the text
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=CHUNK_SIZE,
    chunk_overlap=100,
    length_function=len
)

# Split the text into manageable chunks
chunks = text_splitter.split_text(docs)

# Initialize Qdrant client and embedding model
client = QdrantClient(host='localhost')
embed_model = TextEmbedding()

# Generate embeddings for each text chunk
embeds = embed_model.embed(chunks)

# Prepare payloads for Qdrant
pl_text = []
for index, section in enumerate(chunks):
    payload = {str(index): section}  # Create a payload dictionary for each chunk
    pl_text.append(payload)

# Create a batch of embeddings and payloads for insertion into Qdrant
embeds = models.Batch(
    ids=range(0, len(chunks)),  # Unique IDs for each chunk
    vectors=list(embeds),  # Corresponding vectors for each chunk
    payloads=pl_text  # Metadata payloads for each chunk
)

# Upload the chunks and their embeddings to the specified Qdrant collection
client.upsert(
    collection_name=collect,
    points=embeds
)