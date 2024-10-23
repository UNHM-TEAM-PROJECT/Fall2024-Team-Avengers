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


# Expected responses for Page 2
expected_responses_page2 = {
    "What are the activities planned for Week 1?": [
        "Class Introduction", "Development Team (DT) Setup", "Introduction to Project Management", "Introduction to Scrum workflow", "Project Goal"
    ],
    "When is the Project Kickoff?": ["Week 2 (9/4)"],
    "When does the first sprint start?": ["Week 4 (9/18)"],
    "How often are scrum meetings held during the first sprint?": ["Initially, Monday, Wednesday, and Friday"],
    "When is the end of the first sprint?": ["Week 6 (10/2)"],
    "What happens during the Sprint Retrospective?": ["The sprint is reviewed", "areas for improvement are identified"],
    "When is the second sprint planning meeting?": ["Week 7 (10/9)"],
    "When does the second sprint start?": ["Week 7 (10/9)"],
    "Are there any changes to the scrum meeting schedule during the second sprint?": [
        "Yes", "schedule varies", "sometimes meetings are held only on Mondays", "other times on multiple days of the week"
    ],
    "When is Thanksgiving break?": ["The week of November 20th"],
    "What is covered during Week 3?": [
        "Sprint Planning meeting", "creation of Sprint Backlog", "user stories", "tasks", "bugs", "team communication", "integration with source code control"
    ],
    "When do the scrum meetings switch to happening only on Mondays?": ["During Week 6 (10/2)", "Week 11 (11/6)"],
    "What are the activities for the week of 10/2?": [
        "Scrum meetings (Monday only)", "end of the first sprint", "sprint review", "retrospective"
    ],
    "When is the Sprint Review for the first sprint?": ["Week 6 (10/2)"],
    "What happens during the week of 9/11?": [
        "Creation of Sprint Backlog", "user stories", "tasks", "bugs", "integration with source code control", "team communication"
    ],
    "When does the third sprint start?": ["Week 12 (11/13)"],
    "Are there any changes to the scrum meetings for week 13?": ["Yes", "meetings are held Monday, Wednesday, and Friday"],
    "What tools are used for project management in this course?": ["Jira"],
    "What is the purpose of the Sprint Planning meeting?": ["To create a plan for the upcoming sprint", "based on the Product Backlog"]
}

# Test function for Page 2
@pytest.mark.parametrize("question, expected_keywords", expected_responses_page2.items())
def test_chatbot_page2_responses(question, expected_keywords):
    response = get_response(question)  # Call the real model function
    # Check that at least one expected keyword is in the response
    assert any(keyword in response for keyword in expected_keywords), f"For '{question}', expected one of {expected_keywords} but got '{response}'"
