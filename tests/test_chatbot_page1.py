import sys
import os
import pytest

# Add project directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from chatbot_fat import get_response, main


# Fixture for setup
@pytest.fixture(scope="module", autouse=True)
def setup_chatbot():
    pdf_path = './qdrant/2024-fall-comp690-M2-M3-jin-1.pdf'
    main(pdf_path)  # Initialize chatbot with the provided PDF


# Expected responses for Page 1
expected_responses_page1 = {
    "What time?": ["The M2 section is Wednesday from 9:10 AM to 12:00 PM", "M3 section is Wednesday from 1:10 PM to 4:00 PM"],
    "Office hours?": ["Professor Karen Jin's office hours are Monday from 1:00 PM to 4:00 PM", "Friday from 9:00 AM to 12:00 PM"],
    "Where’s the class?": ["Room P142"],
    "How many credits?": ["4 credits"],
    "Is there a Zoom link?": ["Yes, the Zoom link for Professor Karen Jin’s office hours is Join our Cloud HD Video Meeting"],
    "Who's the instructor?": ["Professor Karen Jin", "Associate Professor in the Department of Applied Engineering and Sciences"],
    "When is Karen Jin's office hours?": ["Monday 1:00 PM to 4:00 PM", "Friday 9:00 AM to 12:00 PM"],
    "What time does the M2 section start on Wednesday?": ["9:10 AM"],
    "How can I schedule an appointment with Professor Jin?": ["Email Professor Jin at karen.jin@unh.edu"],
    "Where is Professor Jin's office located?": ["Room 139, Pandora Mill building"],
    "What is the professor's email address?": ["karen.jin@unh.edu"],
    "What room is the class in?": ["Room P142"],
    "Can I meet the professor on Monday afternoon?": ["Yes, during office hours from 1:00 PM to 4:00 PM"],
    "Will Professor Jin be available on Fridays?": ["Yes, from 9:00 AM to 12:00 PM"],
    "How do I join the professor's Zoom for office hours?": ["Use this link: Join our Cloud HD Video Meeting"],
    "Can I make an appointment outside of office hours?": ["Yes, email Professor Jin at karen.jin@unh.edu"],
    "Can I email the professor to set up a meeting?": ["Yes, email her at karen.jin@unh.edu"],
    "What kind of projects will we do in this internship?": ["Team-based projects involving real-world IT products, processes, or services with external stakeholders"],
    "Wht is prof jin's email?": ["karen.jin@unh.edu"],
    "When are ofice hurs for prof Jin?": ["Monday 1:00 PM to 4:00 PM", "Friday 9:00 AM to 12:00 PM"]
}

# Test function for Page 1
@pytest.mark.parametrize("question, expected_keywords", expected_responses_page1.items())
def test_chatbot_page1_responses(question, expected_keywords):
    response = get_response(question)  # Call the real model function
    # Check that at least one expected keyword is in the response
    assert any(keyword in response for keyword in expected_keywords), f"For '{question}', expected one of {expected_keywords} but got '{response}'"
