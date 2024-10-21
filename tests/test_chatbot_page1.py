import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from chatbot_fat import get_response, main

# Fixture for setup
@pytest.fixture(scope="module", autouse=True)
def setup_chatbot():
    pdf_path = './qdrant/2024-fall-comp690-M2-M3-jin-1.pdf'
    main(pdf_path)

# Expected responses for Page 1
expected_responses_page1 = {
    "What's the course name?": ["COMP 893 Team Project Internship"],
    "How many credits is this course?": ["1-3 credits"],
    "When is this course offered?": ["Fall 2024"],
    "Where are classes held?": ["Rm P142"],
    "What time is the M1 section on Wednesdays?": ["9:10 AM to 12:00 PM"],
    "What time is the M2 section on Wednesdays?": ["1:10 PM to 4:00 PM"],
    "Who is the instructor?": ["Professor Karen Jin"],
    "What's the instructor's title?": ["Associate Professor"],
    "What department is the professor in?": ["Department of Applied Engineering and Sciences"],
    "Where is the professor's office?": ["Rm 139, Pandora Mill building"],
    "What is the professor's Zoom link?": ["Join our Cloud HD Video Meeting"],
    "What is the professor's email?": ["karen.jin@unh.edu"],
    "What are the professor's office hours?": ["Monday 1:00 PM to 4:00 PM and Friday 9:00 AM to 12:00 PM"],
    "Are office hours available online?": ["Yes, over Zoom."],
    "How do I schedule an appointment with the professor?": ["Email the professor to make an appointment."],
    "What building is the class in?": ["The syllabus does not specify the building."],
    "What's the course description?": ["[Summarize the course description from page 1]"],
    "What are the student learning outcomes?": ["[List the student learning outcomes from page 1]"],
    "Is there a phone number for the professor?": ["The syllabus does not list a phone number."],
    "What is the professor's full title?": ["Associate Professor, Department of Applied Engineering and Science"]
}

# Test function for Page 1
@pytest.mark.parametrize("question, expected_answers", expected_responses_page1.items())
def test_chatbot_page1_responses(question, expected_answers):
    response = get_response(question)  # Call the real model function
    assert response in expected_answers, f"For '{question}', got '{response}' which was not in expected answers."
