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


# Expected responses for Page 5
expected_responses_page5 = {
    "What questions should be answered in the self-assessment section?": [
        "What you learned", "relationship of the work to your major", "comparison of theory and practice",
        "project's influence on future career plans", "reflection on internship experiences", "advice for a fellow student and/or faculty member"
    ],
    "What comparison should be made in the self-assessment?": [
        "Comparison between theory (classroom learning) and practice (internship experience)"
    ],
    "How should the project's influence on future career plans be discussed?": [
        "Discuss how the project activities and experiences will influence your future career plans"
    ],
    "What reflections on the internship experience should be included?": [
        "What was learned", "how it will be applied to professional career goals", "skills needing development for career readiness", 
        "advice for a fellow student and/or faculty member"
    ],
    "How long should the self-assessment section be (minimum)?": ["A minimum of 3 full pages", "excluding spacing, figures, and tables"],
    "What should be included in the conclusion section?": ["A summary of key conclusions derived from the project experience"],
    "How long should the conclusion section be?": ["1 full page"],
    "What is the required formatting for the internship report (spacing)?": ["Single-spaced"],
    "What is the required page range for the entire report (excluding title page, figures and tables)?": ["Between 6-8 pages"],
    "What font size is required for the report?": ["12-point"],
    "What is the breakdown of grading criteria for the final report?": ["60% content", "20% grammar and mechanics", "20% format"],
    "What is the consequence of failing to meet the page requirements?": ["Up to a 30% deduction from the total report grade"],
    "What is the minimum percentage needed on the final report to pass the course?": ["75%"],
    "Should bullet points be used in the final report?": ["No", "use full sentences"],
    "How are tables and figures to be handled in the report?": ["All tables and figures must be captioned"],
    "Can I use a font other than Times New Roman?": ["No", "Times New Roman is specified"],
    "What is the minimum page length for the conclusion section?": ["1 full page"],
    "What additional skills should be identified for career readiness in the self-assessment?": [
        "Learning a new technology", "developing a broader network", "taking additional coursework"
    ],
    "What advice should be given to a fellow student and/or faculty member?": [
        "Advice related to the student's internship experience", "lessons learned"
    ],
    "What should be included in a reflection on the internship experience?": [
        "A description of what was learned", "how it will be applied to professional career goals", 
        "identification of additional skills that need to be developed for career readiness"
    ]
}

# Test function for Page 5
@pytest.mark.parametrize("question, expected_keywords", expected_responses_page5.items())
def test_chatbot_page5_responses(question, expected_keywords):
    response = get_response(question)  # Call the real model function
    # Check that at least one expected keyword is in the response
    assert any(keyword in response for keyword in expected_keywords), f"For '{question}', expected one of {expected_keywords} but got '{response}'"
