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


# Expected responses for Page 4
expected_responses_page4 = {
    "What is the policy regarding late submissions?": [
        "The policy is very strict", "applies only in exceptional cases", "illness, accident, emergencies", "proper documentation"
    ],
    "Under what circumstances are late submissions considered?": [
        "Only in exceptional cases", "documented student illness", "accident", "emergencies"
    ],
    "What must be included in a request for a late submission?": [
        "An email sent before the deadline", "explaining the circumstances", "providing evidence"
    ],
    "What are the requirements for the final report title page?": [
        "The student's full name", "internship start and finish dates", "project title"
    ],
    "What should be included in the executive summary of the final report?": [
        "A concise overview of the project", "objectives", "duration", "key outcomes"
    ],
    "What should be included in the introduction section of the final report?": [
        "An introduction to the project", "the rationale for using the Scrum framework", "the project's significance"
    ],
    "What should be described in the Project Objectives section?": [
        "Clearly stated objectives", "deliverables", "intended business or customer impact"
    ],
    "How should the use of the Scrum framework be explained in the report?": [
        "Explain how the Scrum framework was adopted", "roles", "responsibilities", "adjustments made"
    ],
    "What should be included in the self-assessment section?": [
        "What you learned", "the relationship of the work to your major", "benefits to you", "comparison of theory and practice", 
        "the project's influence on your future career", "reflections on the internship experience", "advice for fellow students/faculty"
    ],
    "How long should the executive summary be?": ["The prompt doesn't specify length", "it should be concise"],
    "What formatting is required for the final report?": [
        "Single-spaced", "6-8 pages", "12-point Times New Roman", "no extra space between paragraphs", 
        "all tables/figures captioned", "page numbers", "submitted as a PDF"
    ],
    "What is the minimum number of pages required for the self-assessment section?": ["Minimal 3 full pages", "excluding spacing, figures, and tables"],
    "What is the minimum number of full pages required for the final report?": ["Minimal 2 full pages for the executive summary section", "Total report should be 6-8 pages"],
    "What should be included in the conclusion section of the final report?": [
        "A summary of key conclusions derived from the project experience"
    ],
    "What is the required font size and style for the final report?": ["12-point Times New Roman"],
    "How should tables and figures be presented in the report?": ["All tables and figures must be captioned"],
    "What are the grading criteria for the final report?": ["60% content", "20% grammar and mechanics", "20% format"],
    "What is the penalty for not meeting the page requirements?": ["Up to a 30% deduction from the total report grade"],
    "What is the minimum passing grade for the final report?": ["75%"],
    "What file format should the final report be submitted in?": ["PDF"]
}

# Test function for Page 4
@pytest.mark.parametrize("question, expected_keywords", expected_responses_page4.items())
def test_chatbot_page4_responses(question, expected_keywords):
    response = get_response(question)  # Call the real model function
    # Check that at least one expected keyword is in the response
    assert any(keyword in response for keyword in expected_keywords), f"For '{question}', expected one of {expected_keywords} but got '{response}'"
