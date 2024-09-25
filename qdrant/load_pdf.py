""" Script to load pdf into qdrant vector database, needs pdf name as command line argument """
import os
import sys
import PyPDF2
from  qdrant_client import QdrantClient, models
from fastembed import TextEmbedding

CHUNK_SIZE = 1000
def get_docs(pdf_path):
    """ Converts pdf into string of text"""
    text = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        print(len(reader.pages))
    
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            #text = page.extract_text() or ""
            text.append(page.extract_text() or "")
    return text

def path_from_name(file_name):
    """Converts name to file path """
    exec_path = os.path.dirname(__file__)
    file_path = os.path.join(exec_path, file_name)

    return file_path

path = path_from_name(sys.argv[1])

docs = get_docs(path)
client = QdrantClient( host='localhost' )

for num, page in enumerate(docs):
    embed_model = TextEmbedding()
    #words = page.split()

    #word_chunks = [words[i*CHUNK_SIZE:(i+1) * CHUNK_SIZE] for i in range((len(words) + CHUNK_SIZE -1) // CHUNK_SIZE)]

    #chunks = [" ".join(words) for words in word_chunks]
    #print(chunks)

    embeds = embed_model.embed(page)

    #pl_text = []
    #for index, section in enumerate(chunks):
     #   payload = {str(index) : section}
      #  pl_text.append(payload)

    embeds = models.Batch( ids=[num], vectors = list(embeds), payloads = [{"0" : page}])

    client.upsert(collection_name = "internship2024",
                points = embeds
                )
