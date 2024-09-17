import PyPDF2
import os
import sys
from  qdrant_client import QdrantClient, models
from fastembed import TextEmbedding

def get_docs(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
    return text

def path_from_name(file_name):
    exec_path = os.path.dirname(__file__)
    file_path = os.path.join(exec_path, file_name)
   
    return file_path

chunk_size = 200
path = path_from_name(sys.argv[1])

docs = get_docs(path)

words = docs.split()

word_chunks = [words[i*chunk_size:(i+1) * chunk_size] for i in range((len(words) + chunk_size -1) // chunk_size)]

chunks = [" ".join(words) for words in word_chunks]
print(chunks)

client = QdrantClient( host='localhost' )
embed_model = TextEmbedding()

embeds = embed_model.embed(chunks)

text = []
for index, section in enumerate(chunks):
    payload = {str(index) : section}
    text.append(payload)

embeds = models.Batch( ids=range(0, len(chunks)), vectors = list(embeds), payloads = text)

client.upsert(collection_name = "internship2024", 
              points = embeds
             )