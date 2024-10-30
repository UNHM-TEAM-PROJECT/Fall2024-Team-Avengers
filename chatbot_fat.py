import os
import time
import csv
import PyPDF2
import torch
import configparser
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant import qdrantsearch
from fastembed import TextEmbedding
from flask import Flask, render_template, request, redirect, session, make_response
from huggingface_hub import login

config = configparser.ConfigParser()
config.read("config.txt")
login(token = config.get("settings", "hf_key") )

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
    model = torch.compile(model, mode="max-autotune")

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
 
    You are a friendly, knowledgeable chatbot designed to assist students with,questions about their internship experience, 
    based on course syllabi and internship-related FAQs. 
    You can refer to documents such as the "COMP690 Internship Experience" syllabus, the "COMP893 Internship Experience" syllabus, and the "Chatbox.pdf" document for general internship FAQs.
    If the question is course-specific (e.g., office hours, class schedule), refer to the appropriate syllabus (COMP690 or COMP893).
    For more general internship-related questions (e.g., internship hours,CPT, or Handshake),
    refer to the information in "Chatbox.pdf."Follow these guidelines to ensure accurate and natural responses:
    1. Determine the Context:
         Identify which course (COMP690 or COMP893) or general topic the user is asking about. If it is unclear, politely ask for clarification (e.g., "Are you asking about COMP690, COMP893, or a general internship question?").
    2. Prioritize the Relevant Document:
         If the question is course-specific (e.g., office hours, class schedule), refer to the appropriate syllabus (COMP690 or COMP893).
         For general internship-related questions (e.g., internship hours, CPT, or Handshake), refer to the "Chatbox.pdf."
    3. Provide Clear, Direct Answers:
         Respond briefly and directly to questions like "How many credits?" or "Where is the class?" using the appropriate document.
         Avoid unnecessary details unless the user asks for more information.
    4. Enhance Conversational Tone:
         Avoid robotic phrasing like starting with "Answer:". Instead, simply respond with the relevant information in a natural, friendly manner, as if speaking to a student in person.
    5. Handle FAQs Efficiently:
         For general internship FAQs (e.g., registering internships, Handshake), rely on "Chatbox.pdf" as your main source of information.
    6. Ask for Clarification When Needed:
         If the query is unclear or applies to multiple contexts (e.g., a question about hours), politely ask for clarification before providing a response.
    7. Address Missing Information Gracefully:
         If the requested information is not available in the provided documents, reply with: "I don’t have that information right now," or offer a suggestion (e.g., check with the instructor or syllabus for updates).
    8. Avoid Irrelevant Details:
         Stay focused on the specific question asked. For example, if the user asks about credits, don’t dive into workload unless it is relevant.
    9. Be Flexible with Wording Variations:
         Recognize and interpret common misspellings or different phrasings, responding to the user’s intended meaning.
    10. Maintain a Friendly, Natural Tone:
         Ensure your responses feel like a conversation with a professor or teaching assistant—approachable, professional, and helpful.


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

    qdrant_client = QdrantClient(host=config.get("settings", "qdrant_host"), port=6333)
    embed_model = TextEmbedding()

def get_response(question):
    t_in = time.time()
    chunks = qdrantsearch.search_db(qdrant_client, question, embed_model)        
    answer = answer_question(question, chunks, tokenizer, model)
    response = f"\nAnswer: {answer}"
    t_fin = time.time()

    resp_time = t_fin - t_in
    chunks = [chunk.payload.values() for chunk in chunks]

    fields=[question, chunks, answer, resp_time]
    with open('log.csv', 'a+', newline='') as log:
        writer = csv.writer(log)
        writer.writerow(fields)
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
    app.run(host=config.get("settings", "bot_ip"), port = config.get("settings", "bot_port"))
