import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from chatbot_fat import get_response, main

# Fixture for setup
@pytest.fixture(scope="module", autouse=True)
def setup_chatbot():
    pdf_path = './qdrant/2024-fall-comp690-M2-M3-jin-1.pdf'
    main(pdf_path)

# Expected responses for Page 5
expected_responses_page5 = {
    "What should be included in my self-assessment?": [
        "Your self-assessment should address: what you learned, the project's relevance to your major, the benefits you gained, a comparison of theory (classroom learning) and practice (internship experience), how project activities correlated with classroom knowledge, how the project will influence your future career, reflections on your internship experience (including skills needing development), and advice for a fellow student or faculty member."
    ],
    "What comparison should I make in the self-assessment?": [
        "Compare theory (classroom learning) and practice (your internship experiences)."
    ],
    "How should I discuss the project's influence on my future career?": [
        "Explain how the project and internship experiences will affect your future career goals and plans."
    ],
    "What reflections should be included in the self-assessment?": [
        "Describe what you learned, how it will be applied to your career, what additional skills you need to develop, and any advice you would offer to others."
    ],
    "What's the minimum length for the self-assessment section?": [
        "At least 3 full pages (excluding spacing, figures, and tables)."
    ],
    "What should the conclusion section include?": [
        "A summary of key conclusions from your project experience."
    ],
    "How long should the conclusion section be?": [
        "1 full page."
    ],
    "What's the required spacing for the report?": [
        "Single-spaced."
    ],
    "How many pages should the report be (excluding title page, figures, tables)?": [
        "Between 6 and 8 pages."
    ],
    "What font size is required?": [
        "12-point Times New Roman."
    ],
    "What are the grading criteria for the report?": [
        "60% content, 20% grammar and mechanics, 20% format."
    ],
    "What happens if my report is too short?": [
        "Up to a 30% deduction of the total report grade."
    ],
    "What's the minimum grade needed on the final report to pass?": [
        "75%"
    ],
    "Can I use bullet points in my report?": [
        "No, use full sentences."
    ],
    "How should I present tables and figures?": [
        "All tables and figures must be captioned."
    ],
    "Can I use a different font than Times New Roman?": [
        "No, Times New Roman is required."
    ],
    "What's the minimum length for the conclusion?": [
        "1 full page."
    ],
    "What additional skills should I mention for career readiness?": [
        "Mention skills like learning new technologies, networking, or additional coursework."
    ],
    "What kind of advice should I give to others?": [
        "Advice based on your internship experience and what you learned."
    ],
    "What should my reflection on the internship experience cover?": [
        "What you learned, how it applies to your career goals, additional skills needed for career readiness, and any advice for others."
    ]
}

# Test function for Page 5
@pytest.mark.parametrize("question, expected_keywords", expected_responses_page5.items())
def test_chatbot_page5_responses(question, expected_keywords):
    response = get_response(question)  # Call the real model function
    # Check that at least one expected keyword is in the response
    assert any(keyword in response for keyword in expected_keywords), f"For '{question}', expected one of {expected_keywords} but got '{response}'"