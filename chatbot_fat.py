import os
import PyPDF2
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant import qdrantsearch
from fastembed import TextEmbedding
from flask import Flask, render_template, request, redirect, session, make_response
from huggingface_hub import login

login(token = "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")

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("chatbotUI.html")

@app.route('/llm_response', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        message = request.form['message']
        response = make_response(get_response(message))
        response.mimetype = "text/plain"

        return response


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
    quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")

    model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

    model = AutoModelForCausalLM.from_pretrained(
    model_id, torch_dtype=torch.bfloat16, quantization_config=quantization_config)

    tokenizer = AutoTokenizer.from_pretrained(model_id)

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
    messages = [
    {"role": "system", "content": f"""
 
    You are a friendly, knowledgeable chatbot designed to help students by answering questions based on the "COMP690 Internship Experience" course syllabus.
    Your role is to provide clear, concise, and accurate information to students in a conversational tone, similar to how a professor or teaching assistant would
    respond. Use only the information provided below under "CONTEXT" to answer the student's question

    Answer directly and clearly without saying "According to the syllabus."

    Be professional but approachable in your tone.

    If the information is not available in the context, say: "I don’t have that information right now."

    Focus on making responses feel natural, as if you're directly answering the student’s question.


    Context: 
    {chunks[0].payload.values()}
    {chunks[1].payload.values()}

    """},
    {"role": "user", "content": question},
    ]
    inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")
    input_length = inputs.shape[1]
    generated_ids = model.generate(inputs, do_sample=True, max_new_tokens=500)
    return tokenizer.batch_decode(generated_ids[:, input_length:], skip_special_tokens=True)[0]


def main(pdf_path):
    global tokenizer
    global model
    global qdrant_client
    global embed_model

    context = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(context)

    tokenizer, model = load_pretrained_model()

    qdrant_client = QdrantClient(host='localhost', port=6333)
    embed_model = TextEmbedding()

def get_response(question):
    chunks = qdrantsearch.search_db(qdrant_client, question, embed_model)        
    answer = answer_question(question, chunks, tokenizer, model)
    response = f"\nAnswer: {answer}"
    return response

#CLI Interactive loop
#    while True:
#        question = input("\nAsk a question (or type 'exit' to quit): ")
#        if question.lower() == 'exit':
#            print("Goodbye!")
#            break
#        chunks = qdrantsearch.search_db(qdrant_client, question, embed_model)
#        #print(chunks)
#        print(chunks)
#        answer = answer_question(question, chunks, tokenizer, model)
#        response = f"\nAnswer: {answer}"
#        print(response)

if __name__ == "__main__":
    pdf_path = './qdrant/2024-fall-comp690-M2-M3-jin-1.pdf'
    main(pdf_path)
    app.run(host="192.168.122.244", port=80)
