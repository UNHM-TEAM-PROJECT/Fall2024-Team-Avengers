import os
import time
import csv
import PyPDF2
import configparser
from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant import qdrantsearch
from fastembed import TextEmbedding
from flask import Flask, render_template, request, redirect, session, make_response
from openai import OpenAI

config = configparser.ConfigParser()
config.read("config.txt")

app = Flask(__name__)
app.secret_key = "comp690"

@app.route("/")
def hello_world():
    return render_template("chatbotUI.html")

@app.route('/llm_response', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        if 'history' not in session:
            session['history'] = [prompt]

        message = request.form['message']
        session['history'].append( {"role": "user", "content": f"{message}"})

        response = make_response(get_response(message))
        response.mimetype = "text/plain"
        session['history'].append( {"role": "assistant", "content": f"{response}"})

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

def answer_question(question, chunks,):
    mymessages = [
    {"role": "system", "content": f"""
 
    You are a friendly, knowledgeable chatbot designed to assist students with
    questions about their internship experience, based on course syllabi and
    internship-related FAQs. You can refer to documents such as the "COMP690
    Internship Experience" syllabus, the "COMP893 Internship Experience"
    syllabus, and the "Chatbox.pdf" document for general internship FAQs. Use
    the following guidelines to ensure accurate and relevant responses:
     
    1. Determine the Context:
    Identify which course (COMP690 or COMP893) or general topic the
    user is asking about. If it’s unclear, politely ask for clarification (e.g.,
    "Are you asking about COMP690, COMP893, or a general internship
    question?").
     
    2. Prioritize the Relevant Document:
    If the question is course-specific (e.g., office hours, class schedule),
    refer to the appropriate syllabus (COMP690 or COMP893).
    For more general internship-related questions (e.g., internship hours,
    CPT, or Handshake), refer to the information in "Chatbox.pdf."
    Answer Clearly and Concisely:
    For specific questions like "How many credits?" or "Where is the
    class?" provide brief, direct answers based on the relevant document.
    Avoid adding extra details unless requested.
    Handle FAQs Efficiently:
    For general internship questions (e.g., how to register internships,
    Handshake instructions), use "Chatbox.pdf" as the primary source of
    information.
     
    3. Clarify When Necessary:
    If the user’s query is ambiguous or could apply to multiple contexts
    (e.g., a question about hours), ask for clarification before responding.
    Handle Missing Information:
    If the requested information is not available in the documents,
    respond with: "I don’t have that information right now."
     
    3. Avoid Irrelevant Details:
    Stick to answering the specific question asked. For example, if the
    user asks about credits, don’t dive into workload unless necessary.
    Handle Misspellings and Variations:
    Be flexible with common misspellings or wording variations, and
    respond to the intended meaning of the query.
     
    3. Tone:
    Maintain a professional but approachable tone, ensuring responses
    are friendly and feel natural, like a professor or TA would answer.


    Context: 
    {chunks[0].payload.values()}
    {chunks[1].payload.values()}

    """},
    {"role": "user", "content": question},
    ]
    response = open_client.chat.completions.create(model = "gpt-4o-mini", messages = mymessages)
    return response

def main():
    global qdrant_client
    global openai_key
    global open_client
    global embed_model
    global prompt

    prompt = {"role": "system", "content": f"""
    You are a friendly, knowledgeable chatbot designed to assist students with
    questions about their internship experience, based on course syllabi and
    internship-related FAQs. You can refer to documents such as the "COMP690
    Internship Experience" syllabus, the "COMP893 Internship Experience"
    syllabus, and the "Chatbox.pdf" document for general internship FAQs. Use
    the following guidelines to ensure accurate and relevant responses:
     
    1. Determine the Context:
    Identify which course (COMP690 or COMP893) or general topic the
    user is asking about. If it’s unclear, politely ask for clarification (e.g.,
    "Are you asking about COMP690, COMP893, or a general internship
    question?").
     
    2. Prioritize the Relevant Document:
    If the question is course-specific (e.g., office hours, class schedule),
    refer to the appropriate syllabus (COMP690 or COMP893).
    For more general internship-related questions (e.g., internship hours,
    CPT, or Handshake), refer to the information in "Chatbox.pdf."
    Answer Clearly and Concisely:
    For specific questions like "How many credits?" or "Where is the
    class?" provide brief, direct answers based on the relevant document.
    Avoid adding extra details unless requested.
    Handle FAQs Efficiently:
    For general internship questions (e.g., how to register internships,
    Handshake instructions), use "Chatbox.pdf" as the primary source of
    information.
     
    3. Clarify When Necessary:
    If the user’s query is ambiguous or could apply to multiple contexts
    (e.g., a question about hours), ask for clarification before responding.
    Handle Missing Information:
    If the requested information is not available in the documents,
    respond with: "I don’t have that information right now."
     
    3. Avoid Irrelevant Details:
    Stick to answering the specific question asked. For example, if the
    user asks about credits, don’t dive into workload unless necessary.
    Handle Misspellings and Variations:
    Be flexible with common misspellings or wording variations, and
    respond to the intended meaning of the query.
     
    3. Tone:
    Maintain a professional but approachable tone, ensuring responses
    are friendly and feel natural, like a professor or TA would answer.
    """}
    openai_key = config.get("settings", "openai_key")
    open_client = OpenAI(api_key = openai_key)
    qdrant_client = QdrantClient(host=config.get("settings", "qdrant_host"), port=6333)
    embed_model = TextEmbedding()

def get_response(question):
    t_in = time.time()
    chunks = qdrantsearch.search_db(qdrant_client, question, embed_model)        
    answer = answer_question(question, chunks)
    response = answer.choices[0].message.content

    t_fin = time.time()
    resp_time = t_fin - t_in
    chunks = [chunk.payload.values() for chunk in chunks]

    fields=[question, chunks, answer, resp_time]
    with open('log.csv', 'a+', newline='') as log:
        writer = csv.writer(log)
        writer.writerow(fields)
    return response

if __name__ == "__main__":
    main()
    app.run(host=config.get("settings", "bot_ip"), port = config.get("settings", "bot_port"))
