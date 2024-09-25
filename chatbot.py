import os
import PyPDF2
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
    return text

def chunk_text(text, chunk_size=2000):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def load_pretrained_model():
    tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    model = AutoModelForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    return tokenizer, model

def create_collection_if_not_exists(qdrant_client, collection_name):
    try:
        qdrant_client.get_collection(collection_name)
        print(f"Collection '{collection_name}' already exists.")
    except UnexpectedResponse as e:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config = models.VectorParams(size=384, distance=models.Distance.DOT)
            )
        print(f"Collection '{collection_name}' created.")

def answer_question(question, chunks, tokenizer, model):
    best_answer = ""
    best_score = float('-inf')
    for chunk in chunks:
        inputs = tokenizer(question, chunk, return_tensors='pt', truncation=True, max_length=512)
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']
        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        start_scores = outputs.start_logits
        end_scores = outputs.end_logits
        start_index = torch.argmax(start_scores)
        end_index = torch.argmax(end_scores) + 1
        if start_index >= end_index:
            continue
        answer_tokens = input_ids[0][start_index:end_index]
        answer = tokenizer.decode(answer_tokens, skip_special_tokens=True).strip()
        answer_score = start_scores[0][start_index].item() + end_scores[0][end_index - 1].item()
        if answer_score > best_score:
            best_answer = answer
            best_score = answer_score
    return best_answer if best_answer else "Answer not found."

def main(pdf_path):
    context = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(context)

    tokenizer, model = load_pretrained_model()

    qdrant_client = QdrantClient(host='localhost', port=6333)
    collection_name = "pdf_chunks"
    
    create_collection_if_not_exists(qdrant_client, collection_name)

    while True:
        question = input("\nAsk a question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            print("Goodbye!")
            break
        answer = answer_question(question, chunks, tokenizer, model)
        response = f"\nAnswer: {answer}"
        print(response)

if __name__ == "__main__":
    pdf_path = './qdrant/2024-fall-comp690-M2-M3-jin-1.pdf'
    main(pdf_path)
