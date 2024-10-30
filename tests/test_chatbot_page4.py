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

# Expected responses for Page 4
expected_responses_page4 = {
    "What is the policy on late submissions?": ["Very strict; only granted in exceptional, documented cases of illness, accident, or emergency."],
    "When would a late submission be accepted?": ["Only if the student emails before the deadline, explains the circumstances, and provides evidence."],
    "What needs to be in a late submission request?": ["Prior email notification, explanation of circumstances, and supporting evidence."],
    "What's on the title page of the final report?": ["Student's full name, internship start and finish dates, and project title."],
    "What should the executive summary include?": ["A concise overview of the project, including objectives, duration, and key outcomes."],
    "What should the introduction section cover?": ["Project background, rationale for using Scrum, and project significance."],
    "What needs to be in the Project Objectives section?": ["Clearly stated objectives, including deliverables and their impact."],
    "How should the use of the Scrum framework be explained?": ["Describe how Scrum was adopted and implemented; discuss roles, responsibilities, and any adaptations."],
    "What does the self-assessment section need to include?": ["Answers to questions about what was learned, the project's relation to major studies, benefits, comparison of theory and practice, correlation with classroom knowledge, future career plans, reflection on the internship, and advice for others."],
    "How long should the executive summary be?": ["The syllabus states a minimum of 2 full pages for this section (excluding spacing, figures, and tables); it should be concise."],
    "What formatting is required for the final report?": ["Single-spaced, 6-8 pages (excluding title page, figures, and tables), 12-point Times New Roman font, no extra space between paragraphs, all tables/figures captioned, page numbers, and saved as a PDF."],
    "How many pages are needed for the self-assessment?": ["A minimum of 3 full pages (excluding spacing, figures, and tables)."],
    "How long does the entire final report need to be?": ["Between 6-8 pages (excluding title page, figures, and tables)."],
    "What goes in the conclusion section?": ["A summary of key conclusions derived from the project experience."],
    "What font and size should be used?": ["Times New Roman, 12-point."],
    "How should tables and figures be handled?": ["All tables and figures must be captioned."],
    "What are the grading criteria for the final report?": ["60% content, 20% grammar and mechanics, 20% format."],
    "What happens if the page requirements aren't met?": ["Up to a 30% deduction from the total report grade."],
    "What's the minimum grade needed on the final report to pass?": ["75%"],
    "In what format should the final report be submitted?": ["PDF"]
}

# Test function for Page 4
@pytest.mark.parametrize("question, expected_keywords", expected_responses_page4.items())
def test_chatbot_page4_responses(question, expected_keywords):
    response = get_response(question)  # Call the real model function
    # Check that at least one expected keyword is in the response
    assert any(keyword in response for keyword in expected_keywords), f"For '{question}', expected one of {expected_keywords} but got '{response}'"