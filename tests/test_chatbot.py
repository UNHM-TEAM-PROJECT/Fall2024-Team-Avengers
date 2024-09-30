# tests/test_chatbot.py

import os
import sys
import logging
from rapidfuzz import fuzz  # Updated to use rapidfuzz for faster string matching

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pytest
from chatbot import Chatbot
from test_data import test_cases

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def chatbot_instance():
    pdf_path = os.path.join(parent_dir, 'qdrant', '2024-fall-comp690-M2-M3-jin-1.pdf')
    # Initialize Chatbot in mock mode
    chatbot = Chatbot(pdf_path, mock_mode=True)
    return chatbot

@pytest.mark.parametrize("test_case", test_cases)
def test_chatbot_responses(chatbot_instance, test_case):
    question = test_case["question"]
    expected_answer = test_case["expected_answer"]
    
    # Get the chatbot's response
    response = chatbot_instance.get_response(question)
    assert response, f"No response received for question: {question}"
    
    # Use fuzzy string matching to allow for minor variations in the response
    similarity = fuzz.ratio(expected_answer.lower(), response.lower())
    
    # Log the question, expected answer, actual response, and similarity score
    logger.info(f"\nQuestion: {question}")
    logger.info(f"Expected: {expected_answer}")
    logger.info(f"Actual: {response}")
    logger.info(f"Similarity: {similarity}%")
    
    # Define a similarity threshold
    similarity_threshold = 85
    logger.info(f"Similarity threshold: {similarity_threshold}%")
    
    # Set a threshold for similarity (e.g., 85% match)
    assert similarity > similarity_threshold, (
        f"Test failed for question: {question}\n"
        f"Expected: {expected_answer}\nActual: {response}\n"
        f"Similarity: {similarity}%"
    )
